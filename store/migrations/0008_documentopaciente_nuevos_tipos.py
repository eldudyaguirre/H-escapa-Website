from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_documentopaciente"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documentopaciente",
            name="tipo",
            field=models.CharField(
                max_length=40,
                choices=[
                    ("CONSENTIMIENTO_TRATAMIENTO", "Consentimiento para tratamiento"),
                    ("AUTORIZACION_INFORMACION", "Autorización de información"),
                    ("FICHA_ADMISION", "Ficha de admisión"),
                    ("CONFIDENCIALIDAD", "Compromiso de confidencialidad"),
                    ("AUTORIZACION_CONTACTO", "Autorización de contacto"),
                    ("IDENTIFICACION", "Documento de identificación"),
                    ("OTRO", "Otros documentos"),
                ],
            ),
        ),
    ]
