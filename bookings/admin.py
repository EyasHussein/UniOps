from django.contrib import admin
from .models import Booking
# Register your models here.
@admin.register(Booking)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status' ,'classroom', 'booking_date', 'start_time', 'end_time', 'recurring', 'processed_by', 'processed_at', 'created_at')
    list_filter=('status',)