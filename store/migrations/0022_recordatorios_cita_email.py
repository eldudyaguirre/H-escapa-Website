from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0021_bitacora_consultas_tareas"),
    ]

    operations = [
        migrations.AddField(
            model_name="cita",
            name="recordatorio_30_enviado",
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name="cita",
            name="recordatorio_10_enviado",
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name="cita",
            name="recordatorio_5_enviado",
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
