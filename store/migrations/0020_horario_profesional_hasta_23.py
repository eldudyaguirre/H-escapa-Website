from datetime import time

from django.db import migrations, models


def ampliar_cierre_a_23(apps, schema_editor):
    Profesional = apps.get_model("store", "Profesional")
    # Lleva de 22:00 a 23:00 a los profesionales con el cierre ampliado
    # por la migración anterior. Se conservan los demás horarios personalizados.
    Profesional.objects.filter(hora_fin_atencion=time(22, 0)).update(
        hora_fin_atencion=time(23, 0)
    )


def revertir_cierre_a_22(apps, schema_editor):
    Profesional = apps.get_model("store", "Profesional")
    Profesional.objects.filter(hora_fin_atencion=time(23, 0)).update(
        hora_fin_atencion=time(22, 0)
    )


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0019_horario_profesional_hasta_22"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profesional",
            name="hora_fin_atencion",
            field=models.TimeField(default="23:00"),
        ),
        migrations.RunPython(
            ampliar_cierre_a_23,
            revertir_cierre_a_22,
        ),
    ]
