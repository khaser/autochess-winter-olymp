# Generated by Django 4.2.16 on 2024-12-30 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0002_alter_placement_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='positionedfigher',
            name='fighter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battles.fighter'),
        ),
    ]