from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0030_parametros_facturacion"),
    ]

    operations = [
        migrations.RemoveField(model_name="parametrosfacturacion", name="secuencial_retencion"),
        migrations.RemoveField(model_name="parametrosfacturacion", name="secuencial_nota_credito"),
        migrations.RemoveField(model_name="parametrosfacturacion", name="secuencial_nota_debito"),
        migrations.RemoveField(model_name="parametrosfacturacion", name="secuencial_guia_remision"),
        migrations.RemoveField(model_name="parametrosfacturacion", name="secuencial_liquidacion_compra"),
    ]
