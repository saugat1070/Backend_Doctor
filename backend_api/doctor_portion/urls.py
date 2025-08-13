from django.urls import path
from doctor_portion.views import Create_Doctor, Fetch_Doctors, Update_Doctor, Delete_Doctor, Create_Booking, Get_Bookings


urlpatterns = [
    path('create', Create_Doctor.as_view(), name='doctor_create'),
    path('list', Fetch_Doctors.as_view(), name='doctor_list'),
    path('<uuid:id>', Update_Doctor.as_view(), name='doctor_update'),
    path('delete/<uuid:id>', Delete_Doctor.as_view(), name='doctor_delete'),
    path('<uuid:doctor_id>/book', Create_Booking.as_view(), name='booking_create'),
    path('bookings', Get_Bookings.as_view(), name='booking_list'),
]