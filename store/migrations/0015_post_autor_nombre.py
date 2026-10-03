from django.db import migrations, models


def copiar_nombre_autor(apps, schema_editor):
    Post = apps.get_model("store", "Post")
    for post in Post.objects.select_related("autor").all().iterator():
        autor = post.autor
        nombre = ""
        if autor:
            # Los modelos históricos de Django no garantizan métodos personalizados.
            # Usamos únicamente campos disponibles en la migración.
            partes = [
                getattr(autor, "first_name", "") or "",
                getattr(autor, "last_name", "") or "",
            ]
            nombre = " ".join(parte.strip() for parte in partes if parte.strip())
            if not nombre:
                nombre = getattr(autor, "username", "") or getattr(autor, "email", "") or ""
        if nombre:
            Post.objects.filter(pk=post.pk).update(autor_nombre=nombre)


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0014_etiquetas_blog_iniciales"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="autor_nombre",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.RunPython(copiar_nombre_autor, migrations.RunPython.noop),
    ]
