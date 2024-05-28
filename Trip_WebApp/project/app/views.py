from django.shortcuts import render, redirect, HttpResponse
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

        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\.com$', email):
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
        return render(request,'add_trip.html',context=context)

@require_POST
def add_trip_details(request):
    try:
        if request.method == 'POST':

            latest_trip = Trip.objects.aggregate(Max('trip_no'))
            latest_trip_number = latest_trip['trip_no__max']

            if latest_trip_number:
                trip_number = int(latest_trip_number[2:]) + 1
            else:
                trip_number = 1

            trip_no = 'TR{:03d}'.format(trip_number)

            trip_type = request.POST.get('trip_type')
            date_str = request.POST.get('date')
            vehicle_name = request.POST.get('vehicle_name')
            vehicle_number = request.POST.get('vehicle_number')
            fixed_charge = request.POST.get('fixed_charge')
            max_km = request.POST.get('max_km')
            extra_charge = request.POST.get('extra_charge')
            driver_name = request.POST.get('driver_name')
            guest_name = request.POST.get('guest_name')
            start_km = request.POST.get('start_km')
            end_km = request.POST.get('end_km')
            start_place = request.POST.get('start_place')
            time = request.POST.get('time')
            destination = request.POST.get('destination')
            time_arrival = request.POST.get('time_arrival')
            arrival_date = request.POST.get('arrival_date')
            trip_days = request.POST.get('trip_days')
            tot_charge = request.POST.get('tot_charge')
            advance = request.POST.get('advance')
            balance = request.POST.get('balance')
            toll = request.POST.getlist('toll')
            guide_fee = request.POST.getlist('guide_fee')
            additional_charges = request.POST.getlist('additional_charges')

            vehicle_number_pattern = re.compile(r'^[A-Z]{2}\d{2}\s[A-Z]{2}\s\d{4}$')
            if not vehicle_number_pattern.match(vehicle_number):
                messages.error(request, 'Invalid vehicle number format. It should be in the format Eg:"KL04 AH 1647".')
                return redirect('add_trip')

            try:
                date = parse_date(date_str)
                arrival_date = parse_date(arrival_date)
                if not (date and arrival_date):
                    raise ValueError
            except (ValueError, TypeError):
                messages.error(request, 'Invalid date format. Date must be in YYYY-MM-DD format.')
                return redirect('add_trip')

            trip = Trip(
                trip_type=trip_type,
                trip_no=trip_no,
                date=date,
                vehicle_name=vehicle_name,
                vehicle_number=vehicle_number,
                fixed_charge=fixed_charge,
                max_km=max_km,
                extra_charge=extra_charge,
                driver_name=driver_name,
                guest_name=guest_name,
                start_km=start_km,
                end_km=end_km,
                start_place=start_place,
                time=time,
                destination=destination,
                time_arrival=time_arrival,
                arrival_date=arrival_date,
                trip_days=trip_days,
                tot_charge=tot_charge,
                advance=advance,
                balance=balance,
            )
            trip.save()

            messages.success(request, 'Trip added successfully.')
            return redirect('add_trip')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('add_trip')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('add_trip')
    

def all_trips(request):
    # Get all trips
    trip = Trip.objects.all()

    # Generate the latest trip number
    latest_trip = Trip.objects.aggregate(Max('trip_no'))
    latest_trip_number = latest_trip['trip_no__max']

    if latest_trip_number:
        trip_number = int(latest_trip_number[2:]) + 1
    else:
        trip_number = 1

    # Format the trip number
    trip_no = 'TR{:03d}'.format(trip_number)

    # Pass the trip and trip_no variables in the context dictionary
    context = {'trip': trip, 'trip_no': trip_no}
    return render(request, 'all_trips_table.html', context=context)



def logout(request):
    auth.logout(request)
    return redirect('home')









