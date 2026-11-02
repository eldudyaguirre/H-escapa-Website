from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0025_videollamada_cita"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cita",
            name="videollamada_sala",
        ),
        migrations.AddField(
            model_name="cita",
            name="google_calendar_event_id",
            field=models.CharField(blank=True, editable=False, max_length=255),
        ),
        migrations.AddField(
            model_name="cita",
            name="google_meet_url",
            field=models.URLField(blank=True, editable=False, max_length=500),
        ),
    ]
