from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #! get the room list
    path('', views.building_list, name = 'rooms'),

    #! BUILDING_ROOMS
    path('building/<int:building_id>/', views.room_list, name='building_rooms'),

    #! ROOM SCHEDULE
    path('schedule/<int:pk>/', views.room_schedule, name='room_schedule'),

    #! ADD ROOM
    path("add/", views.add_room, name = "add_room"),

    #! UPDATE ROOM
    path("update/<int:pk>/", views.update_room, name = "update_room"),
    
    #! Delete Room
    path('delete/<int:pk>/', views.delete_room, name="delete_room"),
]
