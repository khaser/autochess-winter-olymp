# Generated by Django 4.2.16 on 2024-12-30 17:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0007_alter_battle_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='battle',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
