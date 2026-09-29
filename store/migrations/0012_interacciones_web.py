from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0011_completar_datos_y_seguridad_profesional"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="InteraccionWeb",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tipo", models.CharField(choices=[("CONTACTO", "Contacto"), ("AGENDAMIENTO", "Solicitud de agendamiento")], max_length=20)),
                ("nombres", models.CharField(max_length=100)),
                ("apellidos", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("telefono", models.CharField(max_length=30)),
                ("servicio", models.CharField(blank=True, max_length=150)),
                ("fecha_solicitada", models.DateField(blank=True, null=True)),
                ("mensaje", models.TextField(blank=True)),
                ("estado", models.CharField(choices=[("PENDIENTE", "Pendiente"), ("CONTACTADO", "Contactado"), ("CONFIRMADO", "Confirmado"), ("NO_CONCRETADO", "No concretado")], default="PENDIENTE", max_length=20)),
                ("observaciones", models.TextField(blank=True)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Interacción web",
                "verbose_name_plural": "Interacciones web",
                "ordering": ["-creado_en"],
            },
        ),
        migrations.CreateModel(
            name="InteraccionWebHistorial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("estado_anterior", models.CharField(max_length=20)),
                ("estado_nuevo", models.CharField(max_length=20)),
                ("comentario", models.TextField(blank=True)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("interaccion", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="historial", to="store.interaccionweb")),
                ("usuario", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Historial de interacción web",
                "verbose_name_plural": "Historial de interacciones web",
                "ordering": ["-creado_en"],
            },
        ),
        migrations.AddIndex(model_name="interaccionweb", index=models.Index(fields=["tipo", "estado"], name="store_inter_tipo_est_9d9c7b_idx")),
        migrations.AddIndex(model_name="interaccionweb", index=models.Index(fields=["email"], name="store_inter_email_0c2e5d_idx")),
        migrations.AddIndex(model_name="interaccionweb", index=models.Index(fields=["-creado_en"], name="store_inter_creado_7d2eaf_idx")),
    ]
