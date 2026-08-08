from django.db import models

#! Class rooms and status


class Building(models.Model):
    # Keep `building` value for backward compatibility with existing records.
    BUILDING_TYPES = [
        ("building", "Academic Building"),
        ("administration", "Administration Building"),
        ("library", "Library Building"),
        ("service", "Service Building"),
        ("cafeteria", "Cafeteria"),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    building_type = models.CharField(max_length=20, choices=BUILDING_TYPES, default="building")
    
    def __str__(self):
        return self.name

class Room(models.Model):
    STATUS_CHOICES =[
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('under_maintenance', 'Under Maintenance'),
    ]
    
    ROOM_TYPES = [
        ('lecture', 'Lecture'),
        ('lab', 'Laboratory'),
        ('meeting', 'Meeting Room'),
        ('library', 'Library Room'),
        ('auditorium', 'Auditorium'),
        ('other', 'Other'),
    ]

    # University policy: these spaces are visible in inventory but not reservable.
    NON_BOOKABLE_ROOM_TYPES = {"library"}
    NON_BOOKABLE_BUILDING_TYPES = {"cafeteria"}
    
    building = models.ForeignKey(
        Building, 
        on_delete=models.CASCADE, 
        null=True, blank=True, 
        related_name= "rooms"
    )
    room_name = models.CharField(max_length=50, verbose_name='Room Number')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES,  default='lecture')
    capacity = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='available')
    location = models.CharField(max_length=100, blank=True)
    equipment = models.TextField(blank=True)

    @property
    def is_bookable(self):
        if self.room_type in self.NON_BOOKABLE_ROOM_TYPES:
            return False
        if self.building and self.building.building_type in self.NON_BOOKABLE_BUILDING_TYPES:
            return False
        return True

    @property
    def non_bookable_reason(self):
        if self.room_type == "library":
            return "Library spaces are for open study and are not reserved through room booking."
        if self.building and self.building.building_type == "cafeteria":
            return "Cafeteria spaces are service areas and cannot be booked as classrooms."
        return ""
    
    # def __init__(self):
    #     return f"{self.room_name} - ({self.status})"
    
    def __str__(self):
        if self.building:
            return f"{self.room_name} - {self.building.name}"
        return self.room_name #! for the [ForignKey]
    
