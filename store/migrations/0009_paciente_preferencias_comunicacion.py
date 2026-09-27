from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0008_documentopaciente_nuevos_tipos"),
    ]

    operations = [
        migrations.AddField(
            model_name="paciente",
            name="recibir_recordatorios_citas",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="paciente",
            name="recibir_notificaciones_resultados",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="paciente",
            name="recibir_notificaciones_recetas",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="paciente",
            name="recibir_boletin_novedades",
            field=models.BooleanField(default=False),
        ),
    ]
