# Generated manually for the independent electronic-invoicing customer registry.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0026_google_meet_cita"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClienteFacturacion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tipo_identificacion", models.CharField(choices=[("04", "RUC"), ("05", "Cédula"), ("06", "Pasaporte"), ("07", "Consumidor final")], default="05", max_length=2)),
                ("identificacion", models.CharField(db_index=True, max_length=20)),
                ("razon_social", models.CharField(max_length=200)),
                ("nombres", models.CharField(blank=True, max_length=100)),
                ("apellidos", models.CharField(blank=True, max_length=100)),
                ("correo", models.EmailField(blank=True, max_length=254)),
                ("telefono", models.CharField(blank=True, max_length=30)),
                ("direccion", models.CharField(blank=True, max_length=250)),
                ("ciudad", models.CharField(blank=True, max_length=100)),
                ("provincia", models.CharField(blank=True, max_length=100)),
                ("estado", models.CharField(choices=[("ACTIVO", "Activo"), ("INACTIVO", "Inactivo")], default="ACTIVO", max_length=10)),
                ("observaciones", models.TextField(blank=True)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Cliente de facturación",
                "verbose_name_plural": "Clientes de facturación",
                "ordering": ["razon_social", "identificacion"],
            },
        ),
        migrations.AddConstraint(
            model_name="clientefacturacion",
            constraint=models.UniqueConstraint(fields=("tipo_identificacion", "identificacion"), name="uniq_cliente_fact_id_tipo"),
        ),
    ]
