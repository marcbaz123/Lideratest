# Generated by Django 4.2.6 on 2023-11-01 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lideratest', '0021_resultadosevaluador_completado'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultadosevaluador',
            name='suma_orientacion',
            field=models.IntegerField(default=0),
        ),
    ]