from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from store.models import Cita


RECORDATORIOS = (
    (30, "recordatorio_30_enviado"),
    (10, "recordatorio_10_enviado"),
    (5, "recordatorio_5_enviado"),
)

# La tarea del Programador de Windows se ejecutará cada minuto.
# Se conserva una ventana de dos minutos para tolerar pequeños retrasos del scheduler.
VENTANA_ENVIO = timedelta(minutes=2)
ESTADOS_VALIDOS = ("PROGRAMADA", "CONFIRMADA")


class Command(BaseCommand):
    help = (
        "Envía recordatorios por correo 30, 10 y 5 minutos antes de las citas "
        "programadas o confirmadas."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Muestra los correos que se enviarían, sin enviar ni marcar recordatorios.",
        )

    def handle(self, *args, **options):
        simulacion = options["dry_run"]
        ahora = timezone.now()
        limite = ahora + timedelta(minutes=32)

        citas = (
            Cita.objects
            .select_related("paciente", "profesional")
            .filter(
                estado__in=ESTADOS_VALIDOS,
                fecha_hora__gt=ahora,
                fecha_hora__lte=limite,
                paciente__recibir_recordatorios_citas=True,
            )
            .exclude(paciente__correo="")
            .order_by("fecha_hora")
        )

        enviadas = 0
        simuladas = 0
        errores = 0

        for candidata in citas.iterator():
            for minutos, campo in RECORDATORIOS:
                momento_programado = candidata.fecha_hora - timedelta(minutes=minutos)
                if not (momento_programado <= ahora < momento_programado + VENTANA_ENVIO):
                    continue
                if getattr(candidata, campo):
                    continue

                if simulacion:
                    self.stdout.write(
                        f"[SIMULACIÓN] Cita #{candidata.pk}: "
                        f"correo a {candidata.paciente.correo} "
                        f"({minutos} minutos antes)."
                    )
                    simuladas += 1
                    continue

                try:
                    with transaction.atomic():
                        # El bloqueo evita que dos ejecuciones simultáneas envíen
                        # el mismo recordatorio.
                        cita = (
                            Cita.objects
                            .select_for_update()
                            .select_related("paciente", "profesional")
                            .get(pk=candidata.pk)
                        )
                        ahora_bloqueo = timezone.now()

                        if cita.estado not in ESTADOS_VALIDOS:
                            continue
                        if getattr(cita, campo):
                            continue
                        if not cita.paciente.recibir_recordatorios_citas:
                            continue

                        correo = (cita.paciente.correo or "").strip()
                        if not correo:
                            continue

                        momento_programado = cita.fecha_hora - timedelta(minutes=minutos)
                        if not (
                            momento_programado
                            <= ahora_bloqueo
                            < momento_programado + VENTANA_ENVIO
                        ):
                            continue

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
                        nombre = cita.paciente.nombre
                        profesional = str(cita.profesional)
                        modalidad = cita.get_modalidad_display()

                        asunto = (
                            f"H-Escapa | Recordatorio de tu cita en {minutos} minutos"
                        )
                        mensaje = (
                            f"Hola {nombre},\n\n"
                            f"Te recordamos que tienes una cita en H-Escapa dentro de "
                            f"{minutos} minutos.\n\n"
                            f"Fecha: {fecha_local:%d/%m/%Y}\n"
                            f"Hora: {fecha_local:%H:%M}\n"
                            f"Profesional: {profesional}\n"
                            f"Modalidad: {modalidad}\n\n"
                            "Te esperamos. Si necesitas cambiar tu cita, comunícate "
                            "directamente con el consultorio.\n\n"
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
                        enviadas += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Enviado recordatorio de {minutos} min "
                                f"para cita #{cita.pk} a {correo}."
                            )
                        )
                except CommandError:
                    raise
                except Exception as exc:
                    errores += 1
                    self.stderr.write(
                        self.style.ERROR(
                            f"Error al enviar recordatorio de {minutos} min "
                            f"para cita #{candidata.pk}: {exc}"
                        )
                    )

        if simulacion:
            self.stdout.write(
                self.style.WARNING(
                    f"Simulación terminada. Recordatorios que se enviarían: {simuladas}."
                )
            )
        else:
            self.stdout.write(
                f"Proceso terminado. Correos enviados: {enviadas}. Errores: {errores}."
            )

        if errores:
            raise CommandError(
                f"Se produjeron {errores} errores. Revisa el registro del Programador de tareas."
            )
