# Generated by Django 4.2.6 on 2023-10-29 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lideratest', '0018_task_assigned_to_alter_knowledge_base_id_kbase_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultadosEvaluador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultado', models.CharField(max_length=255)),
                ('calificaciones', models.JSONField()),
                ('total_orientacion_personas', models.FloatField(default=0.0)),
                ('total_orientacion_produccion', models.FloatField(default=0.0)),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lideratest.clase')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
