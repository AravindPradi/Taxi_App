from django.urls import path
from .import views

urlpatterns = [

    path('',views.home,name='home'),

    path('register',views.register,name='register'),

    path('login',views.login_user,name='login'),

    path('logout',views.logout,name='logout'),

    path('add_trip',views.add_trip,name='add_trip'),

    path('add_trip_details',views.add_trip_details,name='add_trip_details'),

    path('all_trip_table',views.all_trip_table,name='all_trip_table'),

    path('trip_view/<int:id>',views.trip_view,name='trip_view'),

    path('delete_trip/<int:id>',views.delete_trip,name='delete_trip'),

    path('get_last_trip_details',views.get_last_trip_details,name='get_last_trip_details'),

    path('update_last_trip_page',views.update_last_trip,name='update_last_trip'),

    path('update_trip/', views.update_trip, name='update_trip'),
    
]