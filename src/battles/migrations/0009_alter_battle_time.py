# Generated by Django 4.2.16 on 2024-12-30 19:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0008_battle_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
