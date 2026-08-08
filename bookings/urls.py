from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_booking, name='bookings'),
    path('edit/<int:pk>/', views.edit_booking, name='edit_booking'),
    path('archive/<int:pk>/', views.archive_booking, name='archive_booking'),
    path('restore/<int:pk>/', views.restore_booking, name='restore_booking'),
    path('status/<int:pk>/', views.update_booking_status, name='update_booking_status'),
    path('details/<int:pk>/', views.booking_details_partial, name='booking_details_partial'),
]