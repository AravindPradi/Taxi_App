# Generated by Django 5.0.6 on 2024-06-21 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_trip_trip_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='arrival_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='time_arrival',
            field=models.TimeField(null=True),
        ),
    ]
