# Generated by Django 4.2.6 on 2023-10-24 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lideratest', '0004_knowledge_base_delete_testresponse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knowledge_base',
            name='task',
        ),
        migrations.RemoveField(
            model_name='knowledge_base',
            name='user',
        ),
    ]
