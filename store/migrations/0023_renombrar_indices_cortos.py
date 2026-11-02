from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0022_recordatorios_cita_email"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="documentopaciente",
            old_name="store_docume_pacient_4a7e1d_idx",
            new_name="docpac_pac_tipo_idx",
        ),
        migrations.RenameIndex(
            model_name="documentopaciente",
            old_name="store_docume_pacient_1f2b6d_idx",
            new_name="docpac_pac_creado_idx",
        ),
        migrations.RenameIndex(
            model_name="interaccionweb",
            old_name="store_inter_tipo_est_9d9c7b_idx",
            new_name="inter_tipo_estado_idx",
        ),
        migrations.RenameIndex(
            model_name="interaccionweb",
            old_name="store_inter_email_0c2e5d_idx",
            new_name="inter_email_idx",
        ),
        migrations.RenameIndex(
            model_name="interaccionweb",
            old_name="store_inter_creado_7d2eaf_idx",
            new_name="inter_creado_idx",
        ),
    ]
