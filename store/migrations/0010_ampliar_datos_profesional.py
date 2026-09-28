from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_especialidad_profesional_fk"),
    ]

    operations = [
        migrations.AddField(
            model_name="profesional",
            name="foto",
            field=models.ImageField(blank=True, null=True, upload_to="profesionales/fotos/"),
        ),
        migrations.AddField(
            model_name="profesional",
            name="cedula",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="profesional",
            name="fecha_nacimiento",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profesional",
            name="genero",
            field=models.CharField(blank=True, choices=[("M", "Masculino"), ("F", "Femenino"), ("O", "Otro"), ("N", "Prefiero no indicar")], max_length=1),
        ),
        migrations.AddField(
            model_name="profesional",
            name="direccion",
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name="profesional",
            name="ciudad",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="profesional",
            name="provincia",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="profesional",
            name="contacto_emergencia_nombre",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="profesional",
            name="contacto_emergencia_telefono",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name="profesional",
            name="contacto_emergencia_relacion",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="profesional",
            name="profesion",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="profesional",
            name="especializacion",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="profesional",
            name="titulo",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="profesional",
            name="institucion_titulo",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name="profesional",
            name="anio_titulo",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profesional",
            name="tipo_licencia",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="profesional",
            name="numero_licencia",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="profesional",
            name="fecha_emision_licencia",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profesional",
            name="fecha_vencimiento_licencia",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profesional",
            name="biografia",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="profesional",
            name="codigo_empleado",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="profesional",
            name="tipo_contrato",
            field=models.CharField(blank=True, choices=[("TIEMPO_COMPLETO", "Tiempo completo"), ("MEDIO_TIEMPO", "Medio tiempo"), ("CONTRATO", "Contrato"), ("TEMPORAL", "Temporal"), ("PRACTICAS", "Prácticas")], max_length=20),
        ),
        migrations.AddField(
            model_name="profesional",
            name="fecha_ingreso",
            field=models.DateField(blank=True, null=True),
        ),
    ]
