from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0031_solo_secuencial_facturas"),
    ]

    operations = [
        migrations.CreateModel(
            name="Factura",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("numero", models.CharField(max_length=17, unique=True)),
                ("fecha_emision", models.DateField(default=django.utils.timezone.localdate)),
                ("ambiente", models.CharField(choices=[("1", "Pruebas"), ("2", "Producción")], default="1", max_length=1)),
                ("tipo_identificacion", models.CharField(choices=[("04", "RUC"), ("05", "Cédula"), ("06", "Pasaporte"), ("07", "Consumidor final")], max_length=2)),
                ("identificacion", models.CharField(max_length=20)),
                ("razon_social", models.CharField(max_length=200)),
                ("correo", models.EmailField(blank=True, max_length=254)),
                ("telefono", models.CharField(blank=True, max_length=30)),
                ("direccion", models.CharField(blank=True, max_length=250)),
                ("subtotal", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("total_iva", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("total", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("estado", models.CharField(choices=[("BORRADOR", "Borrador")], default="BORRADOR", max_length=12)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("cliente_registrado", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="facturas", to="store.clientefacturacion")),
                ("paciente", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="facturas", to="store.paciente")),
            ],
            options={"verbose_name": "Factura", "verbose_name_plural": "Facturas", "ordering": ["-fecha_emision", "-id"]},
        ),
        migrations.CreateModel(
            name="DetalleFactura",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(max_length=30)),
                ("descripcion", models.CharField(max_length=250)),
                ("cantidad", models.DecimalField(decimal_places=2, max_digits=10)),
                ("precio_unitario", models.DecimalField(decimal_places=2, max_digits=12)),
                ("tarifa_iva", models.CharField(max_length=2)),
                ("porcentaje_iva", models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ("base_imponible", models.DecimalField(decimal_places=2, max_digits=12)),
                ("valor_iva", models.DecimalField(decimal_places=2, max_digits=12)),
                ("total_linea", models.DecimalField(decimal_places=2, max_digits=12)),
                ("factura", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="detalles", to="store.factura")),
                ("servicio_producto", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="store.servicioproducto")),
            ],
            options={"verbose_name": "Detalle de factura", "verbose_name_plural": "Detalles de factura", "ordering": ["id"]},
        ),
    ]
