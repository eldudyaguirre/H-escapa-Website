from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0029_tarifa_iva_sin_inventario"),
    ]

    operations = [
        migrations.CreateModel(
            name="ParametrosFacturacion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("establecimiento", models.CharField(default="001", max_length=3)),
                ("punto_emision", models.CharField(default="001", max_length=3)),
                ("ambiente", models.CharField(choices=[("1", "Pruebas"), ("2", "Producción")], default="1", max_length=1)),
                ("tipo_emision", models.CharField(choices=[("1", "Emisión normal")], default="1", max_length=1)),
                ("secuencial_factura", models.CharField(default="000000001", max_length=9)),
                ("secuencial_retencion", models.CharField(default="000000001", max_length=9)),
                ("secuencial_nota_credito", models.CharField(default="000000001", max_length=9)),
                ("secuencial_nota_debito", models.CharField(default="000000001", max_length=9)),
                ("secuencial_guia_remision", models.CharField(default="000000001", max_length=9)),
                ("secuencial_liquidacion_compra", models.CharField(default="000000001", max_length=9)),
                ("firma_nombre_archivo", models.CharField(blank=True, max_length=255)),
                ("firma_archivo_cifrado", models.BinaryField(blank=True, null=True)),
                ("clave_firma_cifrada", models.TextField(blank=True)),
                ("firma_vencimiento", models.DateField(blank=True, null=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Parámetros de facturación",
                "verbose_name_plural": "Parámetros de facturación",
            },
        ),
    ]
