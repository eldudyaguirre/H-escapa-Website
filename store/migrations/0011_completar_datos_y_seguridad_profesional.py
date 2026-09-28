from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0010_ampliar_datos_profesional"),
    ]

    operations = [
        migrations.AddField(
            model_name="profesional",
            name="codigo_postal",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="profesional",
            name="pais",
            field=models.CharField(blank=True, default="Ecuador", max_length=100),
        ),
        migrations.AddField(
            model_name="profesional",
            name="forzar_cambio_clave",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="profesional",
            name="dos_factores",
            field=models.BooleanField(default=False),
        ),
    ]
