from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from store.models import Cita


RECORDATORIOS_PACIENTE = (
    (30, "recordatorio_30_enviado"),
    (10, "recordatorio_10_enviado"),
    (5, "recordatorio_5_enviado"),
)
RECORDATORIOS_PROFESIONAL = (
    (10, "recordatorio_profesional_10_enviado"),
    (5, "recordatorio_profesional_5_enviado"),
)

# El Programador de Windows ejecuta el comando cada minuto.
# La ventana absorbe pequeños retrasos del Programador de tareas.
VENTANA_ENVIO = timedelta(minutes=2)
ESTADOS_VALIDOS = ("PROGRAMADA", "CONFIRMADA")


def _enviar_recordatorio(cita_id, minutos, campo, destinatario_tipo):
    """Envía un aviso independiente y marca su entrega bajo bloqueo de la cita."""
    with transaction.atomic():
        cita = (
            Cita.objects
            .select_for_update()
            .select_related("paciente", "profesional", "profesional__usuario")
            .get(pk=cita_id)
        )
        ahora = timezone.now()

        if cita.estado not in ESTADOS_VALIDOS or getattr(cita, campo):
            return False

        momento_programado = cita.fecha_hora - timedelta(minutes=minutos)
        if not (momento_programado <= ahora < momento_programado + VENTANA_ENVIO):
            return False

        if destinatario_tipo == "paciente":
            if not cita.paciente.recibir_recordatorios_citas:
                return False
            correo = (cita.paciente.correo or "").strip()
            nombre_destinatario = cita.paciente.nombre
            saludo = f"Hola {nombre_destinatario},"
            asunto = f"H-Escapa | Recordatorio de tu cita en {minutos} minutos"
            cuerpo_inicial = (
                f"Te recordamos que tienes una cita en H-Escapa dentro de "
                f"{minutos} minutos."
            )
        else:
            correo = (cita.profesional.usuario.email or "").strip()
            nombre_destinatario = str(cita.profesional)
            saludo = f"Hola {nombre_destinatario},"
            asunto = f"H-Escapa | Cita en {minutos} minutos"
            cuerpo_inicial = (
                f"Te recordamos que tienes una cita asignada dentro de "
                f"{minutos} minutos."
            )

        if not correo:
            return False

        remitente = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER
        if not remitente:
            raise CommandError(
                "Falta configurar DEFAULT_FROM_EMAIL o EMAIL_HOST_USER."
            )
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            raise CommandError(
                "Faltan EMAIL_HOST_USER o EMAIL_HOST_PASSWORD en el archivo .env."
            )

        fecha_local = timezone.localtime(cita.fecha_hora)
        modalidad = cita.get_modalidad_display()
        profesional = str(cita.profesional)
        paciente = cita.paciente.nombre

        if destinatario_tipo == "paciente":
            detalles = (
                f"Profesional: {profesional}\n"
                f"Modalidad: {modalidad}\n"
            )
        else:
            detalles = (
                f"Paciente: {paciente}\n"
                f"Teléfono del paciente: {cita.paciente.telefono or 'No registrado'}\n"
                f"Modalidad: {modalidad}\n"
            )

        mensaje = (
            f"{saludo}\n\n"
            f"{cuerpo_inicial}\n\n"
            f"Fecha: {fecha_local:%d/%m/%Y}\n"
            f"Hora: {fecha_local:%H:%M}\n"
            f"{detalles}\n"
            "H-Escapa"
        )

        resultado = send_mail(
            subject=asunto,
            message=mensaje,
            from_email=remitente,
            recipient_list=[correo],
            fail_silently=False,
        )
        if resultado != 1:
            raise RuntimeError(
                f"El servidor de correo no confirmó el envío a {correo}."
            )

        setattr(cita, campo, True)
        cita.save(update_fields={campo, "actualizado_en"})
        return correo


class Command(BaseCommand):
    help = (
        "Envía recordatorios al paciente (30, 10 y 5 minutos antes) y al "
        "profesional (10 y 5 minutos antes) de las citas programadas o confirmadas."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Muestra los correos que se enviarían, sin enviarlos ni marcar avisos.",
        )

    def handle(self, *args, **options):
        simulacion = options["dry_run"]
        ahora = timezone.now()
        limite = ahora + timedelta(minutes=32)

        citas = (
            Cita.objects
            .select_related("paciente", "profesional", "profesional__usuario")
            .filter(
                estado__in=ESTADOS_VALIDOS,
                fecha_hora__gt=ahora,
                fecha_hora__lte=limite,
            )
            .order_by("fecha_hora")
        )

        enviadas = 0
        simuladas = 0
        errores = 0

        for candidata in citas.iterator():
            for minutos, campo_paciente in RECORDATORIOS_PACIENTE:
                momento = candidata.fecha_hora - timedelta(minutes=minutos)
                if not (momento <= ahora < momento + VENTANA_ENVIO):
                    continue

                destinos = [
                    ("paciente", campo_paciente),
                ]
                campo_profesional = dict(RECORDATORIOS_PROFESIONAL).get(minutos)
                if campo_profesional:
                    destinos.append(("profesional", campo_profesional))

                for tipo, campo in destinos:
                    if getattr(candidata, campo):
                        continue

                    if tipo == "paciente":
                        habilitado = candidata.paciente.recibir_recordatorios_citas
                        correo = (candidata.paciente.correo or "").strip()
                    else:
                        habilitado = True
                        correo = (
                            candidata.profesional.usuario.email or ""
                        ).strip()

                    if not habilitado or not correo:
                        continue

                    if simulacion:
                        self.stdout.write(
                            f"[SIMULACIÓN] Cita #{candidata.pk}: "
                            f"{tipo} {correo}, {minutos} minutos antes."
                        )
                        simuladas += 1
                        continue

                    try:
                        correo_enviado = _enviar_recordatorio(
                            candidata.pk,
                            minutos,
                            campo,
                            tipo,
                        )
                        if correo_enviado:
                            enviadas += 1
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Enviado recordatorio de {minutos} min "
                                    f"para cita #{candidata.pk} al {tipo}: "
                                    f"{correo_enviado}."
                                )
                            )
                    except CommandError:
                        raise
                    except Exception as exc:
                        errores += 1
                        self.stderr.write(
                            self.style.ERROR(
                                f"Error en recordatorio de {minutos} min "
                                f"para cita #{candidata.pk}, destinatario "
                                f"{tipo}: {exc}"
                            )
                        )

        if simulacion:
            self.stdout.write(
                self.style.WARNING(
                    f"Simulación terminada. Correos que se enviarían: {simuladas}."
                )
            )
        elif enviadas or errores:
            self.stdout.write(
                f"Proceso terminado. Correos enviados: {enviadas}. Errores: {errores}."
            )

        if errores:
            raise CommandError(
                f"Se produjeron {errores} errores. Revisa el registro del Programador de tareas."
            )
