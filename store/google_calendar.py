"""
Integración de Google Calendar para generar reuniones únicas de Google Meet.
Se utiliza la API REST para mantener la integración ligera y evitar dependencias
adicionales de cliente de Google.
"""
import os
import time
from datetime import timedelta
from urllib.parse import quote
from uuid import uuid4

import requests
from django.utils import timezone


GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_CALENDAR_API = "https://www.googleapis.com/calendar/v3"
GOOGLE_CALENDAR_SCOPE = "https://www.googleapis.com/auth/calendar.events"
GOOGLE_TIMEOUT = (8, 30)


class GoogleCalendarError(Exception):
    """Error controlado de configuración o comunicación con Google Calendar."""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


def obtener_configuracion_oauth():
    client_id = os.getenv("GOOGLE_CALENDAR_CLIENT_ID", "").strip()
    client_secret = os.getenv("GOOGLE_CALENDAR_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        raise GoogleCalendarError(
            "Configura GOOGLE_CALENDAR_CLIENT_ID y GOOGLE_CALENDAR_CLIENT_SECRET."
        )
    return {"client_id": client_id, "client_secret": client_secret}


def google_calendar_oauth_configurado():
    return bool(
        os.getenv("GOOGLE_CALENDAR_CLIENT_ID", "").strip()
        and os.getenv("GOOGLE_CALENDAR_CLIENT_SECRET", "").strip()
    )


def google_calendar_configurado():
    return (
        google_calendar_oauth_configurado()
        and bool(os.getenv("GOOGLE_CALENDAR_REFRESH_TOKEN", "").strip())
    )


def obtener_access_token():
    config = obtener_configuracion_oauth()
    refresh_token = os.getenv("GOOGLE_CALENDAR_REFRESH_TOKEN", "").strip()
    if not refresh_token:
        raise GoogleCalendarError(
            "La cuenta de Google Calendar todavía no está autorizada. "
            "Conecta la cuenta desde el módulo de consultas virtuales."
        )

    try:
        response = requests.post(
            GOOGLE_TOKEN_URL,
            data={
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
            timeout=GOOGLE_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise GoogleCalendarError(
            "No fue posible conectar con el servicio de autorización de Google."
        ) from exc

    if not response.ok:
        try:
            error = response.json().get("error", "")
        except ValueError:
            error = ""
        if error in {"invalid_grant", "invalid_client"}:
            raise GoogleCalendarError(
                "La autorización de Google ya no es válida. Vuelve a conectar "
                "la cuenta de Google Calendar desde el módulo de consultas virtuales."
            )
        raise GoogleCalendarError(
            "Google no pudo renovar la autorización de Calendar."
        )

    try:
        access_token = response.json()["access_token"]
    except (ValueError, KeyError) as exc:
        raise GoogleCalendarError(
            "Google devolvió una respuesta de autorización incompleta."
        ) from exc
    return access_token


def _calendar_request(method, endpoint, access_token, params=None, payload=None):
    url = f"{GOOGLE_CALENDAR_API}/{endpoint.lstrip('/')}"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params or {},
            json=payload,
            timeout=GOOGLE_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise GoogleCalendarError(
            "No fue posible comunicarse con Google Calendar."
        ) from exc

    if not response.ok:
        try:
            data = response.json()
            detail = data.get("error", {}).get("message", "")
        except (ValueError, AttributeError):
            detail = ""
        if response.status_code == 404:
            raise GoogleCalendarError("El evento de Google Calendar no existe.", 404)
        if response.status_code == 401:
            raise GoogleCalendarError(
                "Google rechazó la autorización. Vuelve a conectar la cuenta.",
                401,
            )
        if response.status_code == 403:
            raise GoogleCalendarError(
                "La cuenta no tiene permisos para crear eventos o Google Calendar "
                "API no está habilitada en el proyecto.",
                403,
            )
        mensaje = "Google Calendar rechazó la operación."
        if detail:
            mensaje = f"{mensaje} Detalle: {detail[:240]}"
        raise GoogleCalendarError(mensaje, response.status_code)

    if response.status_code == 204 or not response.content:
        return {}
    try:
        return response.json()
    except ValueError as exc:
        raise GoogleCalendarError(
            "Google Calendar devolvió una respuesta que no se pudo interpretar."
        ) from exc


def _obtener_enlace_meet(evento):
    conference = evento.get("conferenceData") or {}
    for entry in conference.get("entryPoints") or []:
        uri = (entry.get("uri") or "").strip()
        if entry.get("entryPointType") == "video" and uri.startswith(
            "https://meet.google.com/"
        ):
            return uri
    hangout_link = (evento.get("hangoutLink") or "").strip()
    if hangout_link.startswith("https://meet.google.com/"):
        return hangout_link
    return ""


def _obtener_estado_conferencia(evento):
    conference = evento.get("conferenceData") or {}
    request_data = conference.get("createRequest") or {}
    status = request_data.get("status") or {}
    return status.get("statusCode", "")


def _datos_evento(cita):
    inicio = timezone.localtime(cita.fecha_hora)
    fin = timezone.localtime(
        cita.fecha_hora + timedelta(minutes=(cita.duracion_minutos or 60))
    )
    correo_paciente = (cita.paciente.correo or "").strip()
    correo_profesional = (
        cita.profesional.usuario.email or ""
    ).strip()

    if not correo_paciente:
        raise GoogleCalendarError(
            "El paciente no tiene un correo electrónico registrado."
        )
    if not correo_profesional:
        raise GoogleCalendarError(
            "El profesional asignado no tiene un correo electrónico registrado."
        )

    asistentes = []
    vistos = set()
    for correo in (correo_paciente, correo_profesional):
        clave = correo.casefold()
        if clave not in vistos:
            asistentes.append({"email": correo})
            vistos.add(clave)

    return {
        "summary": "Consulta virtual H-Escapa",
        "description": (
            "Consulta virtual programada por H-Escapa. "
            "Utiliza el enlace de Google Meet incluido en esta invitación. "
            "Por privacidad, no se incluyen datos clínicos en el evento."
        ),
        "start": {
            "dateTime": inicio.isoformat(),
            "timeZone": "America/Guayaquil",
        },
        "end": {
            "dateTime": fin.isoformat(),
            "timeZone": "America/Guayaquil",
        },
        "attendees": asistentes,
        "visibility": "private",
        "guestsCanInviteOthers": False,
        "guestsCanModify": False,
        "guestsCanSeeOtherGuests": False,
    }


def crear_o_actualizar_evento_meet(cita):
    """
    Crea un evento privado con una conferencia Meet única o actualiza el evento
    ya asociado a la cita. Los asistentes se invitan solo cuando Meet está listo.
    Devuelve event_id, meet_url y conference_status.
    """
    access_token = obtener_access_token()
    payload = _datos_evento(cita)
    asistentes = payload.pop("attendees")
    evento = None
    ya_tenia_meet = False

    if cita.google_calendar_event_id:
        event_id = quote(cita.google_calendar_event_id, safe="")
        try:
            evento_actual = _calendar_request(
                "GET",
                f"calendars/primary/events/{event_id}",
                access_token,
            )
        except GoogleCalendarError as exc:
            if exc.status_code != 404:
                raise
            evento_actual = None

        if evento_actual and evento_actual.get("status") != "cancelled":
            ya_tenia_meet = bool(_obtener_enlace_meet(evento_actual))
            estado = _obtener_estado_conferencia(evento_actual)
            if not ya_tenia_meet and estado == "failure":
                payload["conferenceData"] = {
                    "createRequest": {
                        "requestId": uuid4().hex,
                        "conferenceSolutionKey": {"type": "hangoutsMeet"},
                    }
                }
            cuerpo_actualizacion = dict(payload)
            if ya_tenia_meet:
                cuerpo_actualizacion["attendees"] = asistentes
            evento = _calendar_request(
                "PATCH",
                f"calendars/primary/events/{event_id}",
                access_token,
                params={
                    "sendUpdates": "all" if ya_tenia_meet else "none",
                    "conferenceDataVersion": 1,
                },
                payload=cuerpo_actualizacion,
            )

    if evento is None:
        cuerpo_creacion = dict(payload)
        cuerpo_creacion["conferenceData"] = {
            "createRequest": {
                "requestId": uuid4().hex,
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
            }
        }
        evento = _calendar_request(
            "POST",
            "calendars/primary/events",
            access_token,
            params={"sendUpdates": "none", "conferenceDataVersion": 1},
            payload=cuerpo_creacion,
        )

    event_id = evento.get("id") or cita.google_calendar_event_id
    if not event_id:
        raise GoogleCalendarError(
            "Google Calendar no devolvió el identificador del evento."
        )

    meet_url = _obtener_enlace_meet(evento)
    estado = _obtener_estado_conferencia(evento)

    # Google genera Meet de forma asíncrona. Consultamos brevemente; si sigue
    # pendiente guardamos el event_id para continuar sin duplicar reuniones.
    for _ in range(6):
        if meet_url or estado == "failure":
            break
        time.sleep(1)
        event_id_encoded = quote(event_id, safe="")
        evento = _calendar_request(
            "GET",
            f"calendars/primary/events/{event_id_encoded}",
            access_token,
        )
        meet_url = _obtener_enlace_meet(evento)
        estado = _obtener_estado_conferencia(evento)

    # Las invitaciones se envían después de que el enlace Meet exista. Así los
    # participantes reciben desde el primer correo el enlace de acceso correcto.
    if meet_url:
        correos_evento = {
            (asistente.get("email") or "").casefold()
            for asistente in (evento.get("attendees") or [])
        }
        faltan_asistentes = any(
            (asistente["email"] or "").casefold() not in correos_evento
            for asistente in asistentes
        )
        if faltan_asistentes or not ya_tenia_meet:
            cuerpo_invitacion = dict(payload)
            cuerpo_invitacion["attendees"] = asistentes
            event_id_encoded = quote(event_id, safe="")
            evento = _calendar_request(
                "PATCH",
                f"calendars/primary/events/{event_id_encoded}",
                access_token,
                params={"sendUpdates": "all", "conferenceDataVersion": 1},
                payload=cuerpo_invitacion,
            )
            meet_url = _obtener_enlace_meet(evento) or meet_url
            estado = _obtener_estado_conferencia(evento) or "success"

    return {
        "event_id": event_id,
        "meet_url": meet_url,
        "conference_status": estado or ("success" if meet_url else "pending"),
    }

def cancelar_evento_google_calendar(event_id):
    """Elimina el evento de la cita y notifica la cancelación a los invitados."""
    if not event_id:
        return
    access_token = obtener_access_token()
    event_id_encoded = quote(event_id, safe="")
    _calendar_request(
        "DELETE",
        f"calendars/primary/events/{event_id_encoded}",
        access_token,
        params={"sendUpdates": "all"},
    )
