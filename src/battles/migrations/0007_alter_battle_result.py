# Generated by Django 4.2.16 on 2024-12-30 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0006_alter_fighter_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='result',
            field=models.CharField(blank=True, choices=[('red', 'red'), ('blue', 'blue')], max_length=16),
        ),
    ]
