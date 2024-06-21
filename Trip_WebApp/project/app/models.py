from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class Trip(models.Model):
    TRIP_TYPE_CHOICES = (
        ('km', 'Kilometers'),
        ('hour', 'Hours'),
    )

    trip_no = models.CharField(max_length=20, unique=True)  
    trip_type = models.CharField(max_length=10, choices=TRIP_TYPE_CHOICES, default='km')
    date = models.DateField(default=timezone.now)  
    vehicle_number = models.CharField(max_length=20)
    vehicle_name = models.CharField(max_length=50)
    fixed_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_km = models.PositiveIntegerField(blank=True, null=True)  
    extra_charge = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    driver_name = models.CharField(max_length=50)
    guest_name = models.CharField(max_length=50)
    strt_km = models.PositiveIntegerField(blank=True, null=True)  
    end_km = models.PositiveIntegerField(blank=True, null=True)  
    strt_time = models.DateTimeField(blank=True, null=True)  
    end_time = models.DateTimeField(blank=True, null=True)  
    ride_hours = models.DateTimeField(blank=True, null=True)
    strt_place = models.CharField(max_length=100)
    time = models.TimeField()  
    destination = models.CharField(max_length=100)
    time_arrival = models.TimeField(null=True)  
    arrival_date = models.DateField(null=True)  
    trip_days = models.PositiveIntegerField(blank=True,null=True)
    toll = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    guidefee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    add_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tot_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    advance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False) 

    def save(self, *args, **kwargs):
        if self.tot_charge is not None and self.advance is not None:
            self.balance = self.tot_charge - self.advance
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Trip #{self.trip_no} - {self.vehicle_number} ({self.trip_type})"