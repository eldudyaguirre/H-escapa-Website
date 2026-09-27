from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_ampliar_datos_paciente"),
    ]

    operations = [
        migrations.AddField(
            model_name="paciente",
            name="foto_perfil",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="pacientes/fotos/",
            ),
        ),
    ]
