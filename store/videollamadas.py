"""Integración segura de videollamadas con una instancia propia de Jitsi Meet."""
import base64
import hashlib
import hmac
import json
import os
import re
import time
from datetime import timedelta


def obtener_configuracion_jitsi():
    """Obtiene y valida la configuración JWT de una instancia Jitsi autogestionada."""
    domain = (os.getenv("JITSI_DOMAIN") or "").strip().lower().rstrip("/")
    sub = (os.getenv("JITSI_SUB") or "meet.jitsi").strip().lower()
    app_id = (os.getenv("JITSI_APP_ID") or "").strip()
    secret = (os.getenv("JITSI_APP_SECRET") or "").strip()
    if not domain or not app_id or not secret:
        raise ValueError("Falta configurar JITSI_DOMAIN, JITSI_APP_ID y JITSI_APP_SECRET.")
    if "://" in domain or not re.fullmatch(r"[a-z0-9.-]+(?::[0-9]{1,5})?", domain):
        raise ValueError("JITSI_DOMAIN debe contener únicamente el dominio del servidor, sin https:// ni rutas.")
    if not re.fullmatch(r"[a-z0-9.*-]+", sub):
        raise ValueError("JITSI_SUB debe coincidir con el XMPP_DOMAIN de Jitsi o con el subdominio autorizado.")
    if domain == "meet.jit.si":
        raise ValueError("meet.jit.si está destinado a pruebas; configura una instancia Jitsi propia para producción.")
    return {"domain": domain, "sub": sub, "app_id": app_id, "secret": secret}


def hash_token_paciente(token):
    """Almacena únicamente el hash del enlace entregado al paciente."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _base64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def crear_token_jitsi(cita, nombre, correo="", moderator=False):
    """Firma un JWT de corta duración y limitado a la sala de una sola cita."""
    config = obtener_configuracion_jitsi()
    if not cita.videollamada_sala:
        raise ValueError("La cita todavía no tiene una sala virtual generada.")
    ahora = int(time.time())
    fin_cita = cita.fecha_hora + timedelta(minutes=(cita.duracion_minutos or 60) + 30)
    expira = min(int(fin_cita.timestamp()), ahora + 2 * 60 * 60)
    if expira <= ahora:
        raise ValueError("El periodo de acceso a esta videollamada ha finalizado.")
    header = {"alg": "HS256", "typ": "JWT"}
    usuario = {
        "name": (nombre or "Participante")[:120],
        "affiliation": "owner" if moderator else "member",
    }
    if moderator:
        usuario["moderator"] = True
    if correo:
        usuario["email"] = correo[:254]

    payload = {
        "aud": config["app_id"],
        "iss": config["app_id"],
        "sub": config["sub"],
        "room": cita.videollamada_sala,
        "iat": ahora,
        "nbf": ahora - 10,
        "exp": expira,
        "context": {"user": usuario},
    }
    contenido = (
        _base64url(json.dumps(header, separators=(",", ":")).encode("utf-8"))
        + "."
        + _base64url(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    )
    firma = hmac.new(config["secret"].encode("utf-8"), contenido.encode("ascii"), hashlib.sha256).digest()
    return contenido + "." + _base64url(firma)
