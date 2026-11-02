from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0017_cita_especialidad"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cita",
            name="estado",
            field=models.CharField(
                choices=[
                    ("PROGRAMADA", "Programada"),
                    ("CONFIRMADA", "Confirmada"),
                    ("EN_PROGRESO", "En progreso"),
                    ("ATENDIDA", "Atendida"),
                    ("CANCELADA", "Cancelada"),
                    ("NO_ASISTIO", "No asistió"),
                ],
                default="PROGRAMADA",
                max_length=12,
            ),
        ),
    ]
