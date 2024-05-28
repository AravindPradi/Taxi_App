from django.urls import path
from .import views

urlpatterns = [

    path('',views.home,name='home'),

    path('register',views.register,name='register'),

    path('login',views.login_user,name='login'),

    path('logout',views.logout,name='logout'),

    path('add_trip',views.add_trip,name='add_trip'),

    path('add_trip_details',views.add_trip_details,name='add_trip_details'),

    path('all_trip_details',views.all_trips,name='all_trips'),
    
]