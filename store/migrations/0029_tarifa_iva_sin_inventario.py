from django.db import migrations, models


def convertir_tarifas_iva(apps, schema_editor):
    ServicioProducto = apps.get_model("store", "ServicioProducto")
    equivalencias = {
        "0": "0", "0.00": "0",
        "5": "5", "5.00": "5",
        "6": "6", "7": "7",
        "15": "4", "15.00": "4",
    }
    for anterior, nuevo in equivalencias.items():
        ServicioProducto.objects.filter(porcentaje_iva=anterior).update(porcentaje_iva=nuevo)


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0028_servicioproducto"),
    ]

    operations = [
        migrations.RunPython(convertir_tarifas_iva, migrations.RunPython.noop),
        migrations.RemoveField(model_name="servicioproducto", name="controlar_stock"),
        migrations.RemoveField(model_name="servicioproducto", name="stock_actual"),
        migrations.AlterField(
            model_name="servicioproducto",
            name="porcentaje_iva",
            field=models.CharField(
                choices=[
                    ("0", "0%"),
                    ("5", "5%"),
                    ("6", "NO OBJETO IMPUESTO"),
                    ("7", "EXENTO IVA"),
                    ("4", "15%"),
                ],
                default="4",
                max_length=2,
            ),
        ),
    ]
