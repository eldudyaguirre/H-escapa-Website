from datetime import time

from django.db import migrations, models


def ampliar_cierre_predeterminado(apps, schema_editor):
    Profesional = apps.get_model("store", "Profesional")
    # Extender únicamente a los profesionales que conservaban el cierre
    # predeterminado anterior de las 17:00. Se respetan otros horarios personalizados.
    Profesional.objects.filter(hora_fin_atencion=time(17, 0)).update(
        hora_fin_atencion=time(22, 0)
    )


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0018_cita_en_progreso"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profesional",
            name="hora_fin_atencion",
            field=models.TimeField(default="22:00"),
        ),
        migrations.RunPython(
            ampliar_cierre_predeterminado,
            migrations.RunPython.noop,
        ),
    ]
