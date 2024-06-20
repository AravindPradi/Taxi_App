from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login as auth_login 
from django.contrib import auth
from .models import Trip
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_date
from django.db.models import Max
import logging


def home(request):
    return render(request,'home.html')



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        mobile = request.POST['mobile']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        if password != cpassword:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, "Invalid email address!")
            return redirect('register')

        if not re.match(r'^[0-9]{10}$', mobile):
            messages.error(request, "Mobile number must be 10 digits!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already used!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        UserProfile.objects.create(user=user, mobile=mobile)

        messages.success(request, f'Account created for {username}!')
        return redirect('login')  

    return render(request, 'register.html')



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  
            return redirect('add_trip') 
        else:
            messages.error(request, "Incorrect username or password. Please try again.")
            return redirect('login')
    
    return render(request, 'login.html')


def add_trip(request):
    latest_trip = Trip.objects.aggregate(Max('trip_no'))
    latest_trip_number = latest_trip['trip_no__max']

    if latest_trip_number:
        trip_number = int(latest_trip_number[2:]) + 1
    else:
        trip_number = 1

    trip_no = 'TR{:03d}'.format(trip_number)

    context = {
        'latest_trip_number': trip_no
    }
    return render(request, 'add_trip.html', context=context)



from django.urls import reverse
from django.contrib import messages
from .models import Trip
from django.views.decorators.csrf import csrf_protect
from django.utils.dateparse import parse_date, parse_time
from datetime import datetime


@csrf_protect
def add_trip_details(request):
    if request.method == 'POST':
        trip_no = request.POST.get('trip_no')
        date = request.POST.get('date')
        vehicle_number = request.POST.get('vehicle_number')
        vehicle_name = request.POST.get('vehicle_name')
        driver_name = request.POST.get('driver_name')
        guest_name = request.POST.get('guest_name')
        fixed_charge = request.POST.get('fixed_charge')
        max_km = request.POST.get('max_km')
        extra_charge = request.POST.get('extra_charge')
        strt_km = request.POST.get('strt_km')
        end_km = request.POST.get('end_km')
        strt_time = request.POST.get('strt_time')
        end_time = request.POST.get('end_time')
        strt_place = request.POST.get('strt_place')
        time = request.POST.get('time')
        destination = request.POST.get('destination')
        time_arrival = request.POST.get('time_arrival')
        arrival_date = request.POST.get('arrival_date')
        trip_days = request.POST.get('trip_days')
        toll = request.POST.get('toll')
        guidefee = request.POST.get('guidefee')
        add_charges = request.POST.get('add_charges')
        tot_charge = request.POST.get('tot_charge')
        advance = request.POST.get('advance')
        balance = request.POST.get('balance')

        errors = []

        if not trip_no:
            errors.append("Trip number is required")
        if not date:
            errors.append("Date is required")
        if not vehicle_number:
            errors.append("Vehicle number is required")
        if not vehicle_name:
            errors.append("Vehicle name is required")
        if not driver_name:
            errors.append("Driver name is required")
        if not guest_name:
            errors.append("Guest name is required")
        if not fixed_charge:
            errors.append("Fixed charge is required")
        if not max_km:
            errors.append("Max kilometer is required")
        if not extra_charge:
            errors.append("Extra charge per km/hour is required")
        if not strt_place:
            errors.append("Starting place is required")
        if not time:
            errors.append("Time is required")
        if not arrival_date:
            errors.append("Arrival date is required")
        if not trip_days:
            errors.append("Trip days is required")
        if not tot_charge:
            errors.append("Total charge is required")
        if not balance:
            errors.append("Balance amount is required")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(reverse('add_trip_details'))

        try:
            trip = Trip(
                trip_no=trip_no,
                date=parse_date(date),
                vehicle_number=vehicle_number,
                vehicle_name=vehicle_name,
                driver_name=driver_name,
                guest_name=guest_name,
                fixed_charge=fixed_charge,
                max_km=max_km,
                extra_charge=extra_charge,
                strt_km=int(strt_km) if strt_km else None,
                end_km=int(end_km) if end_km else None,
                strt_time=parse_time(strt_time) if strt_time else None,
                end_time=parse_time(end_time) if end_time else None,
                ride_hours=((datetime.combine(datetime.min, parse_time(end_time)) - datetime.combine(datetime.min, parse_time(strt_time))).total_seconds() / 3600) if strt_time and end_time else None,
                strt_place=strt_place,
                time=parse_time(time),
                destination=destination,
                time_arrival=parse_time(time_arrival),
                arrival_date=parse_date(arrival_date),
                trip_days=int(trip_days),
                toll=float(toll) if toll else 0,
                guidefee=float(guidefee) if guidefee else 0,
                add_charges=float(add_charges) if add_charges else 0,
                tot_charge=float(tot_charge),
                advance=float(advance) if advance else 0,
                balance=float(balance)
            )
            trip.save()
            messages.success(request, "Trip details added successfully!")
            return redirect(reverse('add_trip_details'))
        except Exception as e:
            messages.error(request, str(e))
            return redirect(reverse('add_trip_details'))

    if Trip.objects.exists():
        latest_trip = Trip.objects.latest('trip_no').trip_no
        latest_trip_number = f'TR{int(latest_trip[2:]) + 1:03d}'
    else:
        latest_trip_number = 'TR001'
    
    return render(request, 'add_trip.html', {'latest_trip_number': latest_trip_number})




def all_trip_table(request):
    trip  = Trip.objects.all()
    
    context = {'trip':trip}
    return render(request,'all_trips_table.html', context=context)


def trip_view(request,id):
    trip = get_object_or_404(Trip,id=id)
    distance_travelled = trip.end_km - trip.start_km
    context = {'trip':trip,
               'distance_travelled':distance_travelled}
    return render(request,'trip_view.html',context=context)


def logout(request):
    auth.logout(request)
    return redirect('home')



def delete_trip(request,id):
    trip = get_object_or_404(Trip,id=id)
    trip.delete()
    messages.info(request,'{{trip.trip_no}} Deleted successfully')
    return redirect('all_trip_table')


def get_last_trip_details(request):
    try:
        latest_trip = Trip.objects.latest('trip_no')
        trip_data = {
            'trip_no': latest_trip.trip_no,
            'date': latest_trip.date,
            'vehicle_name': latest_trip.vehicle_name,
            'vehicle_number': latest_trip.vehicle_number,
            'fixed_charge': latest_trip.fixed_charge,
            'max_km': latest_trip.max_km,
            'extra_charge': latest_trip.extra_charge,
            'driver_name': latest_trip.driver_name,
            'guest_name': latest_trip.guest_name,
            'start_km': latest_trip.start_km,
            'end_km': latest_trip.end_km,
            'strt_place': latest_trip.strt_place,
            'time': latest_trip.time,
            'destination': latest_trip.destination,
            'time_arrival': latest_trip.time_arrival,
            'arrival_date': latest_trip.arrival_date,
            'trip_days': latest_trip.trip_days,
            'toll': latest_trip.toll,
            'guidefee': latest_trip.guidefee,
            'add_charges': latest_trip.add_charges,
            'tot_charge': latest_trip.tot_charge,
            'advance': latest_trip.advance,
            'balance': latest_trip.balance,
        }
        return JsonResponse(trip_data)
    except Trip.DoesNotExist:
        response_data = {
            'error': 'No trips found in the database.'
        }
        return JsonResponse(response_data, status=404)



def update_last_trip(request):
    return render(request,'update_details.html')







import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_trip(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        trip_id = data.get('trip_no')

        try:
            trip = Trip.objects.get(trip_no=trip_id)
            trip.date = data.get('date')
            trip.vehicle_number = data.get('vehicle_number')
            trip.vehicle_name = data.get('vehicle_name')
            trip.fixed_charge = float(data.get('fixed_charge'))
            trip.max_km = int(data.get('max_km'))
            trip.extra_charge = float(data.get('extra_charge'))
            trip.driver_name = data.get('driver_name')
            trip.guest_name = data.get('guest_name')
            trip.start_km = float(data.get('start_km'))
            trip.end_km = float(data.get('end_km'))
            trip.strt_place = data.get('strt_place')
            trip.time = data.get('time')
            trip.destination = data.get('destination')
            trip.time_arrival = data.get('time_arrival')
            trip.arrival_date = data.get('arrival_date')
            trip.trip_days = int(data.get('trip_days'))
            trip.toll = float(data.get('toll'))
            trip.guidefee = float(data.get('guidefee'))
            trip.add_charges = float(data.get('add_charges'))
            trip.tot_charge = float(data.get('tot_charge'))
            trip.advance = float(data.get('advance'))
            trip.balance = float(data.get('balance'))
            trip.save()

            return JsonResponse({'status': 'success', 'message': 'Trip details updated successfully!'})
        except Trip.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Trip not found.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


