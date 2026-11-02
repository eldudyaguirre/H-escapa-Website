import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0020_horario_profesional_hasta_23"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="historiaclinica",
            name="anotaciones",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="historiaclinica",
            name="sugerencias_proxima_cita",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="historiaclinica",
            name="fecha_proxima_cita",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historiaclinica",
            name="registrado_por",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="registros_clinicos_realizados",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="TareaClinica",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("descripcion", models.CharField(max_length=220)),
                ("detalle", models.TextField(blank=True)),
                ("fecha_limite", models.DateField(blank=True, null=True)),
                ("prioridad", models.CharField(
                    choices=[("BAJA", "Baja"), ("NORMAL", "Normal"), ("ALTA", "Alta")],
                    default="NORMAL",
                    max_length=10,
                )),
                ("estado", models.CharField(
                    choices=[("PENDIENTE", "Pendiente"), ("COMPLETADA", "Completada")],
                    default="PENDIENTE",
                    max_length=12,
                )),
                ("completada_en", models.DateTimeField(blank=True, null=True)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                ("creada_por", models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name="tareas_clinicas_creadas",
                    to=settings.AUTH_USER_MODEL,
                )),
                ("historia", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="tareas",
                    to="store.historiaclinica",
                )),
            ],
            options={
                "verbose_name": "Tarea clínica",
                "verbose_name_plural": "Tareas clínicas",
                "ordering": ["estado", "fecha_limite", "-creado_en"],
            },
        ),
        migrations.AddIndex(
            model_name="tareaclinica",
            index=models.Index(fields=["historia", "estado"], name="store_tareac_histori_9a0f20_idx"),
        ),
        migrations.AddIndex(
            model_name="tareaclinica",
            index=models.Index(fields=["fecha_limite", "estado"], name="store_tareac_fecha_l_2e90e3_idx"),
        ),
    ]
