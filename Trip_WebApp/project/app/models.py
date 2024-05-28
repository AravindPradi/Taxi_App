from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class Trip(models.Model):
    trip_type_choices = [
        ('km', 'Kilometers'),
        ('hour', 'Hours')
    ]

    trip_type = models.CharField(max_length=10, choices=trip_type_choices)  
    trip_no = models.CharField(max_length=100)
    date = models.DateField(null=True)
    vehicle_name = models.CharField(max_length=100,null=True)
    vehicle_number = models.CharField(max_length=100,null=True,blank=True)
    fixed_charge = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    max_km = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    extra_charge = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    driver_name = models.CharField(max_length=100,null=True)
    guest_name = models.CharField(max_length=100,null=True)
    start_km = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    end_km = models.DecimalField(max_digits=10, decimal_places=2)
    start_place = models.CharField(max_length=100,null=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    destination = models.CharField(max_length=100, blank=True, null=True)
    time_arrival = models.CharField(max_length=100, blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)
    trip_days = models.IntegerField(blank=True, null=True)
    tot_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    advance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
