from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_paciente_foto_perfil"),
    ]

    operations = [
        migrations.AddField(
            model_name="paciente",
            name="consumo_drogas",
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
