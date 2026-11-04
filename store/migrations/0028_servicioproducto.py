# Catalog for billable services and products, kept separate from appointment services.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0027_cliente_facturacion"),
    ]

    operations = [
        migrations.CreateModel(
            name="ServicioProducto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(max_length=30, unique=True)),
                ("tipo", models.CharField(choices=[("SERVICIO", "Servicio"), ("PRODUCTO", "Producto")], default="SERVICIO", max_length=10)),
                ("nombre", models.CharField(max_length=180)),
                ("descripcion", models.TextField(blank=True)),
                ("precio", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("porcentaje_iva", models.DecimalField(decimal_places=2, default=15, max_digits=5)),
                ("controlar_stock", models.BooleanField(default=False)),
                ("stock_actual", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("estado", models.CharField(choices=[("ACTIVO", "Activo"), ("INACTIVO", "Inactivo")], default="ACTIVO", max_length=10)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Servicio o producto",
                "verbose_name_plural": "Servicios y productos",
                "ordering": ["tipo", "nombre"],
            },
        ),
    ]
