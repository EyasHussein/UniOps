from django.contrib import admin
from .models import Room, Building
# Register your models here.

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'building_type')
    list_filter=('building_type',)
    search_fields=('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_name', 'building', 'room_type', 'capacity', 'location', 'equipment' ,'status')
    list_filter=('building', 'room_type', 'status')
    search_fields=('room_name', 'building__name', 'location', 'equipment')