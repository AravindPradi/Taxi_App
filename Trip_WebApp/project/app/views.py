from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login as auth_login 
from django.contrib import auth
from .models import Trip
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_date
from django.db.models import Max

from django.views.decorators.csrf import csrf_exempt


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
        trip_type = request.POST.get('trip_type') 
        user = request.user
        if trip_type == 'on':
            trip_type = 'hr'
        
        if trip_type == None:
            trip_type = 'km'
        
        trip_no = request.POST.get('trip_no')
        date = request.POST.get('date')
        vehicle_number = request.POST.get('vehicle_number')
        vehicle_name = request.POST.get('vehicle_name')
        driver_name = request.POST.get('driver_name')
        guest_name = request.POST.get('guest_name')
        fixed_charge = request.POST.get('fixed_charge')
        max_km = request.POST.get('max_km')
        if max_km == '':
            max_km = None
        max_hr = request.POST.get('max_hour')
        if max_hr == '':
            max_hr = None
        extra_charge = request.POST.get('extra_charge')
        strt_km = request.POST.get('strt_km')
        end_km = request.POST.get('end_km')


        strt_time = request.POST.getlist('strt_time[]')
        
        ride_hours = request.POST.getlist('ride_hours[]')
   
        end_time = request.POST.getlist('end_time[]')

        strt_place = request.POST.get('strt_place')
        time = request.POST.get('time')
        destination = request.POST.get('destination')
        if destination == None:
            destination = None
        time_arrival = request.POST.get('time_arrival')
        if time_arrival == '':
            time_arrival = None

        arrival_date = request.POST.get('arrival_date')
        if arrival_date == '':
            arrival_date = None
        trip_days = request.POST.get('trip_days')
        if trip_days == '':
            trip_days = None
            
        toll = tuple(request.POST.getlist('toll[]'))
        permit = request.POST.get('permit')
        parking = tuple(request.POST.getlist('pf[]'))
        print(parking)
        entrance = request.POST.get('entrance')
        guidefee = tuple(request.POST.getlist('guidefee[]'))
        add_charges = tuple(request.POST.getlist('add_charges[]'))
        other_desc = tuple(request.POST.getlist('other_desc[]'))
        print(other_desc)
        print(add_charges)
        if other_desc == '':
            other_desc = None
        tot_charge = request.POST.get('tot_charge')
        advance = request.POST.get('advance')
        balance = request.POST.get('balance')

        errors = []

        required_fields = {
            'Trip type': trip_type,
            'Trip number': trip_no,
            'Date': date,
            'Vehicle number': vehicle_number,
            'Vehicle name': vehicle_name,
            'Driver name': driver_name,
            'Guest name': guest_name,
            'Fixed charge': fixed_charge,
            'Max kilometer': max_km,
            'Extra charge per km/hour': extra_charge,
            'Starting place': strt_place,
            'Total charge': tot_charge,
            'Balance amount': balance
        }

        for field_name, field_value in required_fields.items():
            if not field_value:
                errors.append(f"{field_name} is required")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(reverse('add_trip_details'))

        try:
            trip = Trip.objects.create(
                user=user,
                trip_type=trip_type,
                trip_no=trip_no,
                date=parse_date(date),
                vehicle_number=vehicle_number,
                vehicle_name=vehicle_name,
                driver_name=driver_name,
                guest_name=guest_name,
                fixed_charge=int(fixed_charge) if fixed_charge else 0,
                max_km=int(max_km) if max_km else 0,
                max_hr=float(max_hr) if max_hr else 0,
                extra_charge=float(extra_charge) if extra_charge else 0,
                strt_km=int(strt_km) if strt_km else None,
                end_km=int(end_km) if end_km else None,
                strt_place=strt_place,
                time=parse_time(time),
                destination=destination if destination else None,
                time_arrival=parse_time(time_arrival) if time_arrival else None,
                arrival_date=parse_date(arrival_date) if arrival_date else None,
                trip_days=trip_days if trip_days else 0,
                
                permit = float(permit) if permit else 0,
                entrance=float(entrance) if entrance else 0,
                
                tot_charge=float(tot_charge),
                advance=float(advance) if advance else 0,
                balance=float(balance)
            )
            trip.save()

            
            if len(strt_time) == len(end_time) == len(ride_hours):
                mapped = zip(strt_time,end_time,ride_hours)
                mapped = list(mapped)
                for ele in mapped:
                    if ele[0] == '':
                        strt = None
                    else:
                        strt = None
                        for fmt in ('%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S%z'):
                            try:
                                strt = datetime.strptime(ele[0], fmt)
                                break
                            except ValueError:
                                continue
                    if ele[1] == '':
                        end = None
                        
                    else:
                        end = None
                        for fmt in ('%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S%z'):
                            try:
                                end = datetime.strptime(ele[1], fmt)
                                break
                            except ValueError:
                                continue
                    if ele[2] == '':
                        amt = None
                    else:
                        amt = float(ele[2])

                    TripAdditionalData.objects.create(trip=trip,charge_type='Hour',start_time=strt,end_time=end,amount=amt)

            

            if len(other_desc)==len(add_charges):
                mapped=zip(other_desc,add_charges)
                mapped=list(mapped)
                for ele in mapped:
                    TripAdditionalData.objects.create(trip = trip,charge_type='other_charges',amount=ele[1],desc=ele[0])
                    
            print(parking)
            if parking:
                mapped=zip(parking)
                mapped=list(mapped)
                for ele in mapped:
                    TripAdditionalData.objects.create(trip = trip,charge_type='parking',amount=ele[0])
            
            if toll:
                mapped=zip(toll)
                mapped=list(mapped)
                print(mapped)
                for ele in mapped:
                    TripAdditionalData.objects.create(trip = trip,charge_type='toll',amount=ele[0])   

            if guidefee:
                mapped=zip(guidefee)
                mapped=list(mapped)
                print(mapped)
                for ele in mapped:
                    TripAdditionalData.objects.create(trip = trip,charge_type='guidefee',amount=ele[0])
            messages.success(request, "Trip details added successfully!")      
            
            return redirect(reverse('add_trip_details'))
        
        except ValueError as e:
            messages.error(request, str(e))
            return redirect(reverse('add_trip_details'))
        except Exception as e:
            messages.error(request, str(e))
            return redirect(reverse('add_trip_details'))

    if Trip.objects.filter(user=request.user).exists():
        latest_trip = Trip.objects.filter(user=request.user).latest('trip_no').trip_no
        latest_trip_number = f'TR{int(latest_trip[2:]) + 1:03d}'
    else:
        latest_trip_number = 'TR001'
    
    return render(request, 'add_trip.html', {'latest_trip_number': latest_trip_number})



def all_trip_table(request):
    trip  = Trip.objects.all()
    
    context = {'trip':trip}
    return render(request,'all_trips_table.html', context=context)


def trip_view(request, id):
    trip = get_object_or_404(Trip, id=id)
    additional_data = TripAdditionalData.objects.filter(trip=trip)
    other_charge_list = []
    parking_charge_list = []
    toll_charge_list = []
    guide_fee_list = []
    strt_time_data = []
    end_time_data = []

    for i in additional_data:
        if i.charge_type == 'Hour':
            strt_time_data.append(i)

    for i in additional_data:
        if i.charge_type == 'toll':
            toll_charge_list.append(i)

    for i in additional_data:
        if i.charge_type == 'other_charges':
            other_charge_list.append(i)
        print(other_charge_list)

    for i in additional_data:
        if i.charge_type =='parking':
            parking_charge_list.append(i)

    for i in additional_data:
        if i.charge_type == 'guidefee':
            guide_fee_list.append(i)
    
    
    distance_travelled = None
    if trip.strt_km is not None and trip.end_km is not None:
        distance_travelled = trip.end_km - trip.strt_km

    hours_travelled = 0
    for i in additional_data:
        if i.charge_type == 'Hour':
            if i.amount is not None:  # Check if i.amount is not None
                hours_travelled += i.amount
    
    context = {
        'trip': trip,
        'distance_travelled': distance_travelled,
        'other_charge_list':other_charge_list,
        'parking_charge_list':parking_charge_list,
        'toll_charge_list':toll_charge_list,
        'guide_fee_list':guide_fee_list,
        'hours_travelled':hours_travelled,
        'strt_time_data':strt_time_data
    }
    
    return render(request, 'trip_view.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('home')



def delete_trip(request,id):
    trip = get_object_or_404(Trip,id=id)
    trip.delete()
    messages.info(request,'{{trip.trip_no}} Deleted successfully')
    return redirect('all_trip_table')




from django.core.serializers import serialize
def get_last_trip_details(request):
    try:
        latest_trip = Trip.objects.latest('trip_no')
        additional_data = TripAdditionalData.objects.filter(trip=latest_trip)
        additional_data_json = serialize('json', additional_data)

        print(latest_trip.trip_type)
        trip_data = {
            'trip_type': latest_trip.trip_type,
            'trip_no': latest_trip.trip_no,
            'date': latest_trip.date.strftime('%Y-%m-%d'),  
            'vehicle_name': latest_trip.vehicle_name,
            'vehicle_number': latest_trip.vehicle_number,
            'fixed_charge': latest_trip.fixed_charge,
            'max_km': latest_trip.max_km,
            'extra_charge': latest_trip.extra_charge,
            'driver_name': latest_trip.driver_name,
            'guest_name': latest_trip.guest_name,
            'strt_km': latest_trip.strt_km,
            'end_km': latest_trip.end_km,
            'strt_time': latest_trip.strt_time,
            'end_time': latest_trip.end_time,
            'ride_hours': latest_trip.ride_hours,
            'strt_place': latest_trip.strt_place,
            'time': latest_trip.time,  
            'destination': latest_trip.destination,
            'time_arrival': latest_trip.time_arrival,
            'arrival_date': latest_trip.arrival_date,
            'trip_days': latest_trip.trip_days,
            'toll': latest_trip.toll,
            'permit': latest_trip.permit,
            'guidefee': latest_trip.guidefee,
            'parking': latest_trip.parking,
            'entrance': latest_trip.entrance,
            'tot_charge': latest_trip.tot_charge,
            'advance': latest_trip.advance,
            'balance': latest_trip.balance,
        }

        response_data = {
            'trip_data': trip_data,
            'additional_data': json.loads(additional_data_json)
        }

        return JsonResponse(response_data)
    except Trip.DoesNotExist:
        response_data = {
            'error': 'No trips found in the database.'
        }
        return JsonResponse(response_data, status=404)


from django.core.serializers.json import DjangoJSONEncoder
def update_last_trip(request):
        latest_trip = Trip.objects.latest('trip_no')
        additional_data = TripAdditionalData.objects.filter(trip=latest_trip)
        other_charge_list = []
        parking_charge_list = []
        toll_charge_list = []
        guide_fee_list = []
        hours_total = []

        hours_total = []
        for i in additional_data:
            if i.charge_type == 'Hour':
                if i.start_time is not None and i.end_time is not None and i.amount is not None:
                    hours_total.append([i.start_time.strftime('%Y-%m-%dT%H:%M'), i.end_time.strftime('%Y-%m-%dT%H:%M'), i.amount])


        for i in additional_data:
            if i.charge_type == 'toll':
                toll_charge_list.append(i)
        print(toll_charge_list)
        for i in additional_data:
            if i.charge_type == 'other_charges':
                other_charge_list.append(i)
        print(other_charge_list)

        for i in additional_data:
            if i.charge_type =='parking':
                parking_charge_list.append(i)
        print(parking_charge_list)
        for i in additional_data:
            if i.charge_type == 'guidefee':
                guide_fee_list.append(i)
        print(guide_fee_list)
        latest_trip_json = json.dumps({
            'trip_type': latest_trip.trip_type,
            'trip_no': latest_trip.trip_no,
            'date': latest_trip.date.strftime('%Y-%m-%d'),  
            'vehicle_name': latest_trip.vehicle_name,
            'vehicle_number': latest_trip.vehicle_number,
            'fixed_charge': latest_trip.fixed_charge,
            'max_km': latest_trip.max_km,
            'max_hour':latest_trip.max_hr,
            'extra_charge': latest_trip.extra_charge,
            'driver_name': latest_trip.driver_name,
            'guest_name': latest_trip.guest_name,
            'strt_km': latest_trip.strt_km,
            'end_km': latest_trip.end_km,

            'strt_place': latest_trip.strt_place,
            'time': latest_trip.time,  
            'destination': latest_trip.destination,
            'time_arrival': latest_trip.time_arrival,
            'arrival_date': latest_trip.arrival_date,
            'trip_days': latest_trip.trip_days,
             
            'permit': latest_trip.permit,
            'guide_fee' : latest_trip.guidefee,
           
            'entrance': latest_trip.entrance,
            'tot_charge': latest_trip.tot_charge,
            'advance': latest_trip.advance,
            'balance': latest_trip.balance,
        }, cls=DjangoJSONEncoder)

        print(latest_trip_json)
        return render(request,'update_details.html',{'latest_trip':latest_trip_json,'other_charge_list':other_charge_list,'parking_charge_list':parking_charge_list,'toll_charge_list':toll_charge_list,'guide_fee_list':guide_fee_list,'hours_total':hours_total})





from datetime import datetime


import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_trip(request):
    if request.method == 'POST':
        
            
        
        
        trip_id = request.POST.get('trip_no')

        try:
            trip = Trip.objects.get(trip_no=trip_id)
            trip.date = request.POST.get('date')
            trip.vehicle_number = request.POST.get('vehicle_number')
            trip.vehicle_name = request.POST.get('vehicle_name')
            trip.fixed_charge = float(request.POST.get('fixed_charge'))
            trip.max_km = int(request.POST.get('max_km'))
            trip.extra_charge = float(request.POST.get('extra_charge'))
            trip.driver_name = request.POST.get('driver_name')
            trip.guest_name = request.POST.get('guest_name')
            trip.start_km = request.POST.get('start_km')
            end_km = request.POST.get('end_km')
            trip.end_km = float(end_km) if end_km not in [None, ''] else 0
            trip.strt_place = request.POST.get('strt_place')
            
            if request.POST.get('time') == '':
                trip.time = None
            else:
                trip.time = request.POST.get('time')

            if request.POST.get('destination') == '':
                trip.destination = None
            else:
                trip.destination = request.POST.get('destination')

            
                
            
            strt_time = request.POST.getlist('strt_time[]')
            

            end_time = request.POST.getlist('end_time[]')
           
            
            ride_hours = request.POST.getlist('ride_hours[]')

            if request.POST.get('time_arrival') == '':
                trip.time_arrival = None
            else:
                trip.time_arrival = request.POST.get('time_arrival')

            if request.POST.get('arrival_date') == '':
                trip.arrival_date = None
            else:
                trip.arrival_date = request.POST.get('arrival_date')
            if request.POST.get('trip_days') == '':
                trip.trip_days = None
            else:
                trip.trip_days = int(request.POST.get('trip_days'))
            
            guidefee = request.POST.getlist('guide[]')
            toll = request.POST.getlist('tl[]')
            trip.permit = request.POST.get('permit')
            trip.entrance = request.POST.get('entry')
            
            parking = request.POST.getlist('parking[]')
            other_desc = request.POST.getlist('other_desc[]')
            add_charges = request.POST.getlist('add_charges[]')
            
            trip.tot_charge = float(request.POST.get('tot_charge'))
            trip.advance = float(request.POST.get('advance'))
            trip.balance = request.POST.get('balance')
            trip.save()
            TripAdditionalData.objects.filter(trip=trip).delete()

            if len(strt_time) == len(end_time) == len(ride_hours):
                mapped = zip(strt_time,end_time,ride_hours)
                mapped = list(mapped)
                for ele in mapped:
                    if ele[0] == '':
                        strt = None
                    else:
                        strt = None
                        for fmt in ('%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S%z'):
                            try:
                                strt = datetime.strptime(ele[0], fmt)
                                break
                            except ValueError:
                                continue
                    if ele[1] == '':
                        end = None
                        
                    else:
                        end = None
                        for fmt in ('%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S%z'):
                            try:
                                end = datetime.strptime(ele[1], fmt)
                                break
                            except ValueError:
                                continue
                        print(datetime.strptime(ele[1], '%Y-%m-%dT%H:%M'))
                    if ele[2] == '':
                        amt = None
                    else:
                        amt = float(ele[2])

                    TripAdditionalData.objects.create(trip=trip,charge_type='Hour',start_time=strt,end_time=end,amount=amt)

            if len(other_desc)==len(add_charges):
                mapped=zip(other_desc,add_charges)
                mapped=list(mapped)
                for ele in mapped:
                    TripAdditionalData.objects.create(trip = trip,charge_type='other_charges',amount=ele[1],desc=ele[0])
                    
            print(parking)
            if parking:
                mapped=zip(parking)
                mapped=list(mapped)
                for ele in mapped:
                    TripAdditionalData.objects.create(trip = trip,charge_type='parking',amount=ele[0])
            
            if toll:
                mapped=zip(toll)
                mapped=list(mapped)
                
                for ele in mapped:
                    TripAdditionalData.objects.create(trip = trip,charge_type='toll',amount=ele[0])   

            if guidefee:
                mapped=zip(guidefee)
                mapped=list(mapped)
                
                for ele in mapped:
                    TripAdditionalData.objects.create(trip = trip,charge_type='guidefee',amount=ele[0])

            return JsonResponse({'status': 'success', 'message': 'Trip details updated successfully!'})
        except Trip.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Trip not found.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


