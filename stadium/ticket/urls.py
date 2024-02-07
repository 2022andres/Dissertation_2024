from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('soccer/',views.soccer,name='soccer'),
    path('athletics/',views.athletics,name='athletics'),
    path('stadium/',views.stadium,name='stadium'),
    path('admin1/',views.admin1, name='admin1'),

    path('stadiums/',views.stadiums,name='stadiums'),
    path('edit_stadiums/<int:pk>/',views.edit_stadiums,name='edit_stadiums'),
    path('delete_stadiums/<int:pk>/',views.delete_stadiums,name='delete_stadiums'),

    path('events/',views.events,name='events'),
    path('edit_events/<int:pk>/',views.edit_events,name='edit_events'),
    path('delete_events/<int:pk>/',views.delete_events,name='delete_events'),
    path('view_events/<int:pk>/',views.view_events,name='view_events'),

    path('athletics_event/',views.athletics_event,name='athletics_event'),
    path('delete_athletics_event/<int:pk>/',views.delete_athletics_event,name='delete_athletics_event'),
    path('edit_athletics_event/<int:pk>/',views.edit_athletics_event,name='edit_athletics_event'),
    path('view_athletics_event/<int:pk>/',views.view_athletics_event,name='view_athletics_event'),



    path('seat_type/',views.seat_type, name='seat_type'),
    path('edit_seat_type/<int:pk>/',views.edit_seat_type,name='edit_seat_type'),
    path('delete_seat_type/<int:pk>/',views.delete_seat_type,name='delete_seat_type'),
    path('view_seat_type/<int:pk>/',views.view_seat_type,name='view_seat_type'),

    path('booking/',views.booking, name='booking'),
    path('edit_booking/<int:pk>/',views.edit_booking,name='edit_booking'),
    path('delete_booking/<int:pk>/',views.delete_booking,name='delete_booking'),
    path('view_booking/<int:pk>/',views.view_booking,name='view_booking'),


    path('fixtures/',views.fixtures, name='fixtures'),
    path('fixtures_page/',views.fixtures_page, name='fixtures_page'),
    path('edit_fixtures/<int:pk>/',views.edit_fixtures,name='edit_fixtures'),
    path('delete_fixtures/<int:pk>/',views.delete_fixtures,name='delete_fixtures'),
    path('view_fixtures/<int:pk>/',views.view_fixtures,name='view_fixtures'),

    path('booknow/',views.booknow, name='booknow'),


    path('users/',views.users, name='users'),
    path('delete_users/<int:pk>/',views.delete_users,name='delete_users'),


    # =======================FRONTEND LOGIC===========================
    path('viewbooking/',views.viewbooking, name='viewbooking'),
    path('see_viewbooking/<int:pk>/',views.see_viewbooking, name='see_viewbooking'),
    path('del_front_booking/<int:pk>/',views.del_front_booking,name='del_front_booking'),

   path('generate_qr_code/<int:booking_id>/', views.generate_qr_code, name='generate_qr_code'),
   path('update_button_state/', views.update_button_state, name='update_button_state'),

   path('payment/',views.payment, name='payment'),
   path('check_qr_status/', views.check_qr_status, name='check_qr_status'),






]


