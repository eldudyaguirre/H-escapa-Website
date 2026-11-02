from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0016_agenda_flexible"),
    ]

    operations = [
        migrations.AddField(
            model_name="cita",
            name="especialidad",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="citas",
                to="store.especialidad",
            ),
        ),
    ]
