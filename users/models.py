from django.contrib.auth.models import AbstractUser
from django.db import models

#! for Login and permissions  

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'), #* the first is stored in the database and the second is shown in admin panel
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    department = models.CharField(max_length=100, blank=True, null=True)
    # def __str__(self): #* getter
    #     return f"{self.username} ({self.role})"