from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0032_facturas"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detallefactura",
            name="tarifa_iva",
            field=models.CharField(
                choices=[
                    ("0", "0%"),
                    ("5", "5%"),
                    ("6", "NO OBJETO IMPUESTO"),
                    ("7", "EXENTO IVA"),
                    ("4", "15%"),
                ],
                max_length=2,
            ),
        ),
    ]
