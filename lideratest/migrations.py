from django.db import migrations

def remove_tables(apps, schema_editor):
    # Nombre de las tablas que deseas eliminar
    tables_to_delete = ['auth_user_permission', 'auth_user_groups', 'auth_user_user_permission', 'auth_group']

    # Eliminar las tablas
    for table in tables_to_delete:
        schema_editor.execute(f'DROP TABLE IF EXISTS {table};')

class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),  # Reemplaza 'tu_app' por el nombre de tu aplicación
    ]

    operations = [
        migrations.RunPython(remove_tables),
    ]