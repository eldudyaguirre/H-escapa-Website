from django.db import migrations


def crear_categorias_blog(apps, schema_editor):
    CategoriaBlog = apps.get_model("store", "CategoriaBlog")

    categorias = [
        ("Psicología", "Artículos sobre psicología y procesos terapéuticos."),
        ("Salud mental", "Información y orientación sobre salud mental."),
        ("Ansiedad y estrés", "Recursos para comprender y manejar la ansiedad y el estrés."),
        ("Bienestar emocional", "Hábitos y herramientas para cuidar el bienestar emocional."),
        ("Relaciones y familia", "Contenido sobre relaciones, familia y vínculos."),
        ("Autoestima y crecimiento personal", "Reflexiones y herramientas para el desarrollo personal."),
    ]

    for nombre, descripcion in categorias:
        CategoriaBlog.objects.get_or_create(
            nombre=nombre,
            defaults={"descripcion": descripcion, "activa": True},
        )


def eliminar_categorias_blog(apps, schema_editor):
    CategoriaBlog = apps.get_model("store", "CategoriaBlog")
    nombres = [
        "Psicología",
        "Salud mental",
        "Ansiedad y estrés",
        "Bienestar emocional",
        "Relaciones y familia",
        "Autoestima y crecimiento personal",
    ]
    CategoriaBlog.objects.filter(nombre__in=nombres).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0012_interacciones_web"),
    ]

    operations = [
        migrations.RunPython(crear_categorias_blog, eliminar_categorias_blog),
    ]
