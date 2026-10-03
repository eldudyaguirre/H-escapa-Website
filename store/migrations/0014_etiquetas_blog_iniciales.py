from django.db import migrations
from django.utils.text import slugify


def crear_etiquetas_blog(apps, schema_editor):
    EtiquetaBlog = apps.get_model("store", "EtiquetaBlog")
    etiquetas = [
        "Ansiedad",
        "Salud mental",
        "Bienestar emocional",
        "Estrés",
        "Autocuidado",
        "Psicología",
        "Terapia",
        "Autoestima",
        "Relaciones",
        "Crecimiento personal",
    ]
    for nombre in etiquetas:
        etiqueta, creada = EtiquetaBlog.objects.get_or_create(nombre=nombre)
        if not etiqueta.slug:
            etiqueta.slug = slugify(nombre)
            etiqueta.save(update_fields=["slug"])


def eliminar_etiquetas_blog(apps, schema_editor):
    EtiquetaBlog = apps.get_model("store", "EtiquetaBlog")
    nombres = [
        "Ansiedad", "Salud mental", "Bienestar emocional", "Estrés",
        "Autocuidado", "Psicología", "Terapia", "Autoestima",
        "Relaciones", "Crecimiento personal",
    ]
    EtiquetaBlog.objects.filter(nombre__in=nombres).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0013_categorias_blog_iniciales"),
    ]

    operations = [
        migrations.RunPython(crear_etiquetas_blog, eliminar_etiquetas_blog),
    ]
