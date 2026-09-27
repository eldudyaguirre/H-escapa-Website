from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_paciente_facturacion_ecuador"),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentoPaciente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("CONSENTIMIENTO_TRATAMIENTO", "Consentimiento para tratamiento"),
                            ("AUTORIZACION_INFORMACION", "Autorización de información"),
                            ("IDENTIFICACION", "Documento de identificación"),
                            ("OTRO", "Otros documentos"),
                        ],
                        max_length=40,
                    ),
                ),
                (
                    "archivo",
                    models.FileField(upload_to="pacientes/documentos/"),
                ),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("PENDIENTE", "Pendiente de firma"),
                            ("FIRMADO", "Firmado y cargado"),
                        ],
                        default="FIRMADO",
                        max_length=10,
                    ),
                ),
                ("observaciones", models.TextField(blank=True)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                (
                    "paciente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documentos",
                        to="store.paciente",
                    ),
                ),
            ],
            options={
                "verbose_name": "Documento del paciente",
                "verbose_name_plural": "Documentos del paciente",
                "ordering": ["-creado_en"],
            },
        ),
        migrations.AddIndex(
            model_name="documentopaciente",
            index=models.Index(fields=["paciente", "tipo"], name="store_docume_pacient_4a7e1d_idx"),
        ),
        migrations.AddIndex(
            model_name="documentopaciente",
            index=models.Index(fields=["paciente", "-creado_en"], name="store_docume_pacient_1f2b6d_idx"),
        ),
    ]
