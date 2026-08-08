from django.contrib import admin
from .models import MaintenanceRequest
# Register your models here.
@admin.register(MaintenanceRequest)

class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'classroom', 'department', 'description', 'priority', 'status', 'created_at', 'updated_at')