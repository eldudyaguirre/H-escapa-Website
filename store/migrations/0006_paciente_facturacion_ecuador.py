from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_paciente_consumo_drogas"),
    ]

    operations = [
        migrations.AddField(model_name="paciente", name="tipo_identificacion_facturacion", field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name="paciente", name="identificacion_facturacion", field=models.CharField(blank=True, max_length=13)),
        migrations.AddField(model_name="paciente", name="nombre_facturacion", field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name="paciente", name="correo_facturacion", field=models.EmailField(blank=True, max_length=254)),
        migrations.AddField(model_name="paciente", name="pago_efectivo", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="paciente", name="pago_tarjeta", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="paciente", name="pago_transferencia", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="paciente", name="pago_deposito", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="paciente", name="pago_cheque", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="paciente", name="pago_otros", field=models.BooleanField(default=False)),
    ]
