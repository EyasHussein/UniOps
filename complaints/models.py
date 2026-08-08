from django.db import models
from django.conf import settings
from rooms.models import Room

# Create your models here.


class Complaint(models.Model):
    TYPE_CHOICES = [
        ('cleanliness', 'Cleanliness'),
        ('noise', 'Noise'),
        ('environment', 'Environment'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name= "complaints")
    email = models.EmailField(blank=True, null=True)
    classroom = models.ForeignKey(Room, on_delete=models.SET_NULL, null= True, related_name='complaints')
    complaint_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='other')
    description = models.TextField()
    photo = models.ImageField(upload_to='photos/%d/%m/%y', blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    #! did not migtared yet 
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    # def __str__(self):
    #     return f"Complaint by {self.student_name or self.user}"
