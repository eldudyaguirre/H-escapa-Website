from django.db import migrations, models
import django.db.models.deletion


def migrar_especialidades(apps, schema_editor):
    Especialidad = apps.get_model("store", "Especialidad")
    Profesional = apps.get_model("store", "Profesional")

    nombres = {
        "PSICOLOGIA": "Psicología",
        "PSICOLOGIA_CLINICA": "Psicología Clínica",
        "TERAPIA_FAMILIAR": "Terapia Familiar",
        "TERAPIA_PAREJA": "Terapia de Pareja",
        "OTRA": "Otra",
    }
    especialidades = {}
    for codigo, nombre in nombres.items():
        especialidad = Especialidad.objects.create(nombre=nombre)
        especialidades[codigo] = especialidad.pk

    for profesional in Profesional.objects.all():
        if profesional.especialidad in especialidades:
            profesional.especialidad_nueva_id = especialidades[profesional.especialidad]
            profesional.save(update_fields=["especialidad_nueva"])


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0005_paciente_consumo_drogas"),
        ("store", "0009_paciente_preferencias_comunicacion"),
    ]

    operations = [
        migrations.CreateModel(
            name="Especialidad",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100, unique=True)),
                ("activa", models.BooleanField(default=True)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["nombre"],
                "verbose_name": "Especialidad",
                "verbose_name_plural": "Especialidades",
            },
        ),
        migrations.AddField(
            model_name="profesional",
            name="especialidad_nueva",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="profesionales_nuevo",
                to="store.especialidad",
            ),
        ),
        migrations.RunPython(migrar_especialidades, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="profesional",
            name="especialidad",
        ),
        migrations.RenameField(
            model_name="profesional",
            old_name="especialidad_nueva",
            new_name="especialidad",
        ),
        migrations.AlterField(
            model_name="profesional",
            name="especialidad",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="profesionales",
                to="store.especialidad",
            ),
        ),
    ]
