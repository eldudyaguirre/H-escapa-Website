from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0023_renombrar_indices_cortos"),
    ]

    operations = [
        migrations.AddField(
            model_name="cita",
            name="recordatorio_profesional_10_enviado",
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name="cita",
            name="recordatorio_profesional_5_enviado",
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
