from django.db import migrations, models
import store.models
import django.db.models.deletion


def crear_servicios_iniciales(apps, schema_editor):
    Servicio = apps.get_model("store", "Servicio")
    servicios = [
        ("manual_therapy", "Terapia Individual", 60),
        ("chronic_pain", "Terapia de Pareja", 60),
        ("hand_therapy", "Terapia Infantil o Adolescente", 60),
        ("sports_therapy", "Ansiedad, depresión, estrés, ira", 60),
        ("cupping_therapy", "Evaluaciones Periciales", 60),
        ("laser_therapy", "Mindfulness y meditación", 60),
    ]
    for slug, nombre, duracion in servicios:
        Servicio.objects.get_or_create(slug=slug, defaults={"nombre": nombre, "duracion_minutos": duracion, "activo": True})


def configurar_dias_existentes(apps, schema_editor):
    Profesional = apps.get_model("store", "Profesional")
    Profesional.objects.filter(dias_atencion=[]).update(dias_atencion=[0, 1, 2, 3, 4])


class Migration(migrations.Migration):
    dependencies = [("store", "0015_post_autor_nombre")]

    operations = [
        migrations.CreateModel(
            name="Servicio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("nombre", models.CharField(max_length=150, unique=True)),
                ("duracion_minutos", models.PositiveIntegerField(default=60, help_text="Duración de la sesión, en minutos")),
                ("activo", models.BooleanField(default=True)),
            ],
            options={"ordering": ["nombre"], "verbose_name": "Servicio", "verbose_name_plural": "Servicios"},
        ),
        migrations.AddField(
            model_name="profesional",
            name="dias_atencion",
            field=models.JSONField(blank=True, default=store.models.dias_laborables_default, help_text="Días de atención: 0 lunes ... 6 domingo"),
        ),
        migrations.AddField(
            model_name="profesional",
            name="hora_inicio_atencion",
            field=models.TimeField(default="09:00"),
        ),
        migrations.AddField(
            model_name="profesional",
            name="hora_fin_atencion",
            field=models.TimeField(default="17:00"),
        ),
        migrations.AddField(
            model_name="profesional",
            name="preparacion_minutos",
            field=models.PositiveSmallIntegerField(default=5, help_text="Minutos de preparación después de cada cita"),
        ),
        migrations.AddField(
            model_name="cita",
            name="servicio",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="citas", to="store.servicio"),
        ),
        migrations.AddField(
            model_name="interaccionweb",
            name="hora_solicitada",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="interaccionweb",
            name="profesional_preferido",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="solicitudes_web", to="store.profesional"),
        ),
        migrations.RunPython(crear_servicios_iniciales, migrations.RunPython.noop),
        migrations.RunPython(configurar_dias_existentes, migrations.RunPython.noop),
    ]
