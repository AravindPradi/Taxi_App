# Generated by Django 5.0.6 on 2024-06-26 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_trip_arrival_date_alter_trip_time_arrival'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='ride_hours',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
