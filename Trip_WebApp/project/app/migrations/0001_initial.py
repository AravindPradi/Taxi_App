# Generated by Django 5.0.6 on 2024-06-20 09:14

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_no', models.CharField(max_length=20, unique=True)),
                ('trip_type', models.CharField(choices=[('km', 'Kilometers'), ('hour', 'Hours')], default='km', max_length=10)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('vehicle_number', models.CharField(max_length=20)),
                ('vehicle_name', models.CharField(max_length=50)),
                ('fixed_charge', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_km', models.PositiveIntegerField(blank=True, null=True)),
                ('extra_charge', models.DecimalField(decimal_places=2, max_digits=5)),
                ('driver_name', models.CharField(max_length=50)),
                ('guest_name', models.CharField(max_length=50)),
                ('start_km', models.PositiveIntegerField(blank=True, default=True)),
                ('end_km', models.PositiveIntegerField(blank=True)),
                ('start_hour', models.DateTimeField(blank=True)),
                ('end_hour', models.DateTimeField(blank=True, null=True)),
                ('strt_place', models.CharField(max_length=100)),
                ('time', models.TimeField()),
                ('destination', models.CharField(max_length=100)),
                ('time_arrival', models.TimeField()),
                ('arrival_date', models.DateField()),
                ('trip_days', models.PositiveIntegerField()),
                ('toll', models.DecimalField(decimal_places=2, max_digits=10)),
                ('guidefee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('add_charges', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tot_charge', models.DecimalField(decimal_places=2, max_digits=10)),
                ('advance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
