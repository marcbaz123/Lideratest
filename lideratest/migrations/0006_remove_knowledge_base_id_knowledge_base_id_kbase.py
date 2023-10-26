from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('lideratest', '0005_remove_knowledge_base_task_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knowledge_base',
            name='id',
        ),
    ]
