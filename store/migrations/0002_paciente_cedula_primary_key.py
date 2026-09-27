from django.db import migrations, models


def migrate_patient_pk(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        raise RuntimeError("Esta migración requiere PostgreSQL.")

    sql = r"""
    DO $$
    DECLARE
        fk_name text;
        fk_table text;
    BEGIN
        IF EXISTS (SELECT 1 FROM store_paciente LIMIT 1) THEN
            RAISE EXCEPTION 'No se puede cambiar el PK de Paciente porque ya existen registros. Respaldar/migrar los pacientes primero.';
        END IF;

        -- Quitar temporalmente todas las FK que apuntan a Paciente.
        FOR fk_name, fk_table IN
            SELECT c.conname, cl.relname
            FROM pg_constraint c
            JOIN pg_class cl ON cl.oid = c.conrelid
            WHERE c.contype = 'f'
              AND c.confrelid = 'store_paciente'::regclass
        LOOP
            EXECUTE 'ALTER TABLE ' || quote_ident(fk_table)
                 || ' DROP CONSTRAINT ' || quote_ident(fk_name);
        END LOOP;

        ALTER TABLE store_paciente DROP CONSTRAINT IF EXISTS store_paciente_pkey;
        ALTER TABLE store_paciente ADD COLUMN IF NOT EXISTS cedula varchar(10);
        ALTER TABLE store_paciente DROP COLUMN IF EXISTS id;
        ALTER TABLE store_paciente ALTER COLUMN cedula SET NOT NULL;
        ALTER TABLE store_paciente ADD CONSTRAINT store_paciente_pkey PRIMARY KEY (cedula);

        ALTER TABLE store_cita
            ALTER COLUMN paciente_id TYPE varchar(10)
            USING paciente_id::text;

        ALTER TABLE store_historiaclinica
            ALTER COLUMN paciente_id TYPE varchar(10)
            USING paciente_id::text;

        ALTER TABLE store_cita
            ADD CONSTRAINT store_cita_paciente_cedula_fk
            FOREIGN KEY (paciente_id) REFERENCES store_paciente(cedula)
            DEFERRABLE INITIALLY DEFERRED;

        ALTER TABLE store_historiaclinica
            ADD CONSTRAINT store_historiaclinica_paciente_cedula_fk
            FOREIGN KEY (paciente_id) REFERENCES store_paciente(cedula)
            DEFERRABLE INITIALLY DEFERRED;
    END $$;
    """

    schema_editor.execute(sql)


def reverse_migrate_patient_pk(apps, schema_editor):
    raise RuntimeError(
        "Esta migración no se revierte automáticamente porque implicaría reconstruir "
        "el ID numérico original de los pacientes."
    )


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(
                    migrate_patient_pk,
                    reverse_migrate_patient_pk,
                ),
            ],
            state_operations=[
                migrations.RemoveField(
                    model_name="paciente",
                    name="id",
                ),
                migrations.AddField(
                    model_name="paciente",
                    name="cedula",
                    field=models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
            ],
        ),
    ]
