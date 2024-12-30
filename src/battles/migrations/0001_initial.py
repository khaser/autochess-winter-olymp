# Generated by Django 4.2.16 on 2024-12-30 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fighter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('ARC', 'Archer'), ('BER', 'Berserker'), ('CAV', 'Cavalry'), ('COM', 'Commander'), ('KN', 'Knight'), ('INF', 'Infantryman')], max_length=3)),
                ('ejudge_short_name', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.userinfo', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PositionedFigher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.PositiveIntegerField()),
                ('column', models.PositiveIntegerField()),
                ('fighter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='battles.fighter')),
                ('placement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battles.placement')),
            ],
        ),
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('R', 'Blue'), ('B', 'Red')], max_length=1)),
                ('blue_placement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='battles_as_blue', to='users.userinfo')),
                ('red_placement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='battles_as_red', to='users.userinfo')),
            ],
        ),
    ]
