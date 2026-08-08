from django.contrib import admin
from .models import Notification
# Register your models here.
@admin.register(Notification)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'is_read', 'created_at')