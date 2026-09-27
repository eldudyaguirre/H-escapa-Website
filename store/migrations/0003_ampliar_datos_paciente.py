from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_paciente_cedula_primary_key"),
    ]

    operations = [
        migrations.AddField(model_name="paciente", name="telefono_alternativo", field=models.CharField(max_length=30, blank=True)),
        migrations.AddField(model_name="paciente", name="ciudad", field=models.CharField(max_length=100, blank=True)),
        migrations.AddField(model_name="paciente", name="provincia", field=models.CharField(max_length=100, blank=True)),
        migrations.AddField(model_name="paciente", name="codigo_postal", field=models.CharField(max_length=20, blank=True)),
        migrations.AddField(model_name="paciente", name="estado_civil", field=models.CharField(max_length=20, blank=True)),
        migrations.AddField(model_name="paciente", name="contacto_preferido", field=models.CharField(default="telefono", max_length=10, blank=True)),
        migrations.AddField(model_name="paciente", name="altura_cm", field=models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)),
        migrations.AddField(model_name="paciente", name="peso_kg", field=models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)),
        migrations.AddField(model_name="paciente", name="alergias", field=models.TextField(blank=True)),
        migrations.AddField(model_name="paciente", name="medicamentos_actuales", field=models.TextField(blank=True)),
        migrations.AddField(model_name="paciente", name="condiciones_cronicas", field=models.TextField(blank=True)),
        migrations.AddField(model_name="paciente", name="cirugias_previas", field=models.TextField(blank=True)),
        migrations.AddField(model_name="paciente", name="hospitalizaciones", field=models.TextField(blank=True)),
        migrations.AddField(model_name="paciente", name="antecedentes_familiares", field=models.TextField(blank=True)),
        migrations.AddField(model_name="paciente", name="tabaquismo", field=models.CharField(max_length=10, blank=True)),
        migrations.AddField(model_name="paciente", name="consumo_alcohol", field=models.CharField(max_length=15, blank=True)),
        migrations.AddField(model_name="paciente", name="frecuencia_ejercicio", field=models.CharField(max_length=15, blank=True)),
        migrations.AddField(model_name="paciente", name="habitos_dieteticos", field=models.TextField(blank=True)),
        migrations.AddField(model_name="paciente", name="relacion_emergencia", field=models.CharField(max_length=80, blank=True)),
        migrations.AddField(model_name="paciente", name="correo_emergencia", field=models.EmailField(max_length=254, blank=True)),
        migrations.AddField(model_name="paciente", name="seguro_proveedor", field=models.CharField(max_length=150, blank=True)),
        migrations.AddField(model_name="paciente", name="seguro_poliza", field=models.CharField(max_length=100, blank=True)),
        migrations.AddField(model_name="paciente", name="seguro_grupo", field=models.CharField(max_length=100, blank=True)),
        migrations.AddField(model_name="paciente", name="seguro_titular", field=models.CharField(max_length=150, blank=True)),
        migrations.AddField(model_name="paciente", name="seguro_relacion", field=models.CharField(max_length=30, blank=True)),
        migrations.AddField(model_name="paciente", name="seguro_telefono", field=models.CharField(max_length=30, blank=True)),
        migrations.AddField(model_name="paciente", name="seguro_secundario", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="paciente", name="seguro_secundario_proveedor", field=models.CharField(max_length=150, blank=True)),
        migrations.AddField(model_name="paciente", name="seguro_secundario_poliza", field=models.CharField(max_length=100, blank=True)),
        migrations.AddField(model_name="paciente", name="metodo_facturacion", field=models.CharField(max_length=20, blank=True)),
        migrations.AddField(model_name="paciente", name="pago_online", field=models.BooleanField(default=False)),
    ]
