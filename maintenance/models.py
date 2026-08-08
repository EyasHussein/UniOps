from django.db import models
from django.conf import settings
from rooms.models import Room

class MaintenanceRequest(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('under repair', 'Under Repair'),
        ('fixed', 'Fixed'),
    ]
    
    TYPE_CHOICES =[
        ('electrical', 'Electrical'),
        ('furniture', 'Furniture Damage'),
        ('ac', 'Air Conditioning'),
        ('plumbing', 'Plumbing'),
        ('equipment', 'Equipment Failure'),
        ('network', 'Network / Internet'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='maintenance_requests')
    email = models.EmailField(blank=True, null=True)
    classroom = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='maintenance_requests')
    department = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    photo = models.ImageField(upload_to= 'MaintenancePhotos/%d/%m/%y', null=True,blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    maintenance_type = models.CharField( max_length=20, choices=TYPE_CHOICES, default="other")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    # def __str__(self):
    #     return f"{self.classroom} - {self.status}"
