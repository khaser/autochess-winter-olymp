# Generated by Django 4.2.16 on 2024-12-30 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('battles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placement',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.userinfo'),
        ),
    ]
