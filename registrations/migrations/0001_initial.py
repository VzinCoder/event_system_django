# Generated by Django 5.1.4 on 2025-01-08 23:50

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('birth_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('confirmed', 'Confirmada'), ('pending', 'Pendente'), ('canceled', 'Cancelada')], default='pending', max_length=10)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registrations.participant')),
            ],
        ),
    ]
