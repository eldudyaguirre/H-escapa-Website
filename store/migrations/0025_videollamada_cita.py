from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0024_recordatorios_profesional"),
    ]

    operations = [
        migrations.AddField(
            model_name="cita",
            name="videollamada_sala",
            field=models.CharField(blank=True, editable=False, max_length=64),
        ),
        migrations.AddField(
            model_name="cita",
            name="videollamada_token_paciente_hash",
            field=models.CharField(blank=True, editable=False, max_length=64),
        ),
    ]
