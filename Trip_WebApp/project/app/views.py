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
        return redirect('register')  

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



logger = logging.getLogger(__name__)

def add_trip_details(request):
    logger.debug(request.POST)
    trip_no = request.POST.get('trip_no')  
    trip_type = request.POST.get('trip_type')
    date = request.POST.get('date')
    vehicle_number = request.POST.get('vehicle_number')
    vehicle_name = request.POST.get('vehicle_name')

    fixed_charge = request.POST.get('fixed_charge')
    try:
        fixed_charge = float(fixed_charge)
    except ValueError:
        print('Invalid fixed charge amount')
        messages.error(request, 'Invalid fixed charge amount.')
        return redirect('add_trip_details')  

    max_km = request.POST.get('max_km')
    if trip_type == 'km' and max_km:
        try:
            max_km = int(max_km)
            if max_km <= 0:
                messages.error(request, 'Max kilometer cannot be negative or zero.')
                return redirect('add_trip')  
        except ValueError:
                print('Invalid max km value')
                messages.error(request, 'Invalid max kilometer value.')
                return redirect('add_trip_details')  
        else:
            max_km = None  

        extra_charge = request.POST.get('extra_charge')
        try:
            extra_charge = float(extra_charge)
        except ValueError:
            print('Invalid extra charge amount')
            messages.error(request, 'Invalid extra charge amount.')
            return redirect('add_trip_details')  

        driver_name = request.POST.get('driver_name')
        guest_name = request.POST.get('guest_name')

        start_km = None
        end_km = None
        start_hour = None
        end_hour = None

        if trip_type == 'km':
            start_km = request.POST.get('start_km')
            if start_km:
                try:
                    start_km = int(start_km)
                    if start_km < 0:
                        messages.error(request, 'Starting kilometer cannot be negative.')
                        return redirect('add_trip')  
                except ValueError:
                    print('Invalid starting km value')
                    messages.error(request, 'Invalid starting kilometer value.')
                    return redirect('add_trip')  

            end_km = request.POST.get('end_km')
            if end_km:
                try:
                    end_km = int(end_km)
                    if end_km < start_km:
                        messages.error(request, 'Ending kilometer cannot be less than starting kilometer.')
                        return redirect('add_trip')  
                except ValueError:
                    print('Invlaid ending km value')
                    messages.error(request, 'Invalid ending kilometer value.')
                    return redirect('add_trip')  
        else:
            start_hour = request.POST.get('start_hour')  
            end_hour = request.POST.get('end_hour')  

        strt_place = request.POST.get('strt_place')
        time = request.POST.get('time')  
        destination = request.POST.get('destination')
        time_arrival = request.POST.get('time_arrival')  
        arrival_date = request.POST.get('arrival_date')

        trip_days = request.POST.get('trip_days')
        try:
            trip_days = int(trip_days)
            if trip_days <= 0:
                messages.error(request, 'Number of days cannot be negative or zero.')
                return redirect('add_trip')  
        except ValueError:
            print('Invalid no of days')
            messages.error(request, 'Invalid number of days.')
            return redirect('add_trip')  

        toll = request.POST.get('toll')
        try:
            toll = float(toll)
        except ValueError:
            print('invalid toll amount')
            messages.error(request, 'Invalid toll amount.')
            return redirect('add_trip')  

        guidefee = request.POST.get('guidefee')
        try:
            guidefee = float(guidefee)
        except ValueError:
            print('invalid guide fee')
            messages.error(request, 'Invalid guide fee amount.')
            return redirect('add_trip')  

        add_charges = request.POST.get('add_charges')
        try:
            add_charges = float(add_charges)
        except ValueError:
            print('Invalid additional charges amount')
            messages.error(request, 'Invalid additional charges amount.')
            return redirect('add_trip')  

        tot_charge = request.POST.get('tot_charge')
        try:
            tot_charge = float(tot_charge)
        except ValueError:
            print('Invalid total charge amount')
            messages.error(request, 'Invalid total charge amount.')
            return redirect('add_trip')  

        advance = request.POST.get('advance')
        try:
            advance = float(advance)
        except ValueError:
            print('Invalid advance amount')
            messages.error(request, 'Invalid advance amount.')
            return redirect('add_trip')  

        try:
            new_trip = Trip.objects.create(
                trip_no=trip_no,
                trip_type=trip_type,
                date=date,
                vehicle_number=vehicle_number,
                vehicle_name=vehicle_name,
                fixed_charge=fixed_charge,
                max_km=max_km,
                extra_charge=extra_charge,
                driver_name=driver_name,
                guest_name=guest_name,
                start_km=start_km,
                end_km=end_km,
                start_hour=start_hour,
                end_hour=end_hour,
                strt_place=strt_place,
                time=time,
                destination=destination,
                time_arrival=time_arrival,
                arrival_date=arrival_date,
                trip_days=trip_days,
                toll=toll,
                guidefee=guidefee,
                add_charges=add_charges,
                tot_charge=tot_charge,
                advance=advance,
            )
            new_trip.save()
            
            messages.success(request, f'Trip #{trip_no} added successfully!')
            return redirect('add_trip') 
        except Exception as e:
            print(e)
            messages.error(request, f'An error occurred: {e}')
            return redirect('add_trip')  

    else:
        return redirect('add_trip')




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
    latest_trip = Trip.objects.latest('trip_no')
    trip_data = {
        'trip_no':latest_trip.trip_no,
        'date':latest_trip.date,
        'vehicle_name':latest_trip.vehicle_name,
        'vehicle_number':latest_trip.vehicle_number,
        'fixed_charge':latest_trip.fixed_charge,
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


