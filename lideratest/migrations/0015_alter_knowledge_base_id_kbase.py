# Generated by Django 4.2.6 on 2023-10-26 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lideratest', '0014_knowledge_base_id_kbase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knowledge_base',
            name='id_kbase',
            field=models.AutoField(db_column='id', default=1, primary_key=True, serialize=False),
        ),
    ]
