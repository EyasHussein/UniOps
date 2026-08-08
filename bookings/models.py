from django.db import models
from django.conf import settings
from rooms.models import Room

from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import time

#! Stores who booked which room and when
#! Admin can approve/reject
#! Prevents double bookings later using logic

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    email = models.EmailField(null=True, blank=True)
    classroom = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    recurring = models.BooleanField(default=False)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='processed_bookings'
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    notes = models.TextField()

    class Meta:
        # PERF: Indexes aligned with dashboard filters/sorts and booking conflict checks.
        indexes = [
            models.Index(fields=["is_deleted", "status", "-created_at"]),
            models.Index(fields=["user", "is_deleted", "-created_at"]),
            models.Index(fields=["classroom", "booking_date", "status"]),
        ]

    def clean(self):
        opening_time = time(8, 0)
        closing_time = time(17, 0)

        if self.booking_date and self.booking_date < timezone.localdate():
            raise ValidationError("Booking date cannot be in the past.")

        if self.classroom and not self.classroom.is_bookable:
            raise ValidationError(self.classroom.non_bookable_reason)
        
        if self.start_time < opening_time or self.end_time > closing_time:
            raise ValidationError("Bookings must be between 8:00 AM and 5:00 PM.")
        
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

        if (self.start_time.minute not in (0, 30)) or (self.end_time.minute not in (0, 30)):
            raise ValidationError("Use 30-minute steps only (e.g., 10:00, 10:30, 11:00).")
        
        if self.classroom and self.classroom.status == "under_maintenance":
            raise ValidationError("This room is under maintenance and cannot be booked.")
        
        conflicting_bookings = Booking.objects.filter(
            classroom = self.classroom,
            booking_date = self.booking_date,
            is_deleted=False,
            status__in=["pending", "approved"],
            start_time__lt = self.end_time,
            end_time__gt = self.start_time
        ).exclude(pk=self.pk)
        
        if conflicting_bookings.exists():
            raise ValidationError("This room already has a pending or approved booking for that time.")
    
    
    def approve(self, admin_user):
        self.full_clean()
        self.status = "approved"
        self.processed_by = admin_user
        self.processed_at = timezone.now()
        self.save()
        
    def reject(self, admin_user):
        self.status = "rejected"
        self.processed_by = admin_user
        self.processed_at = timezone.now()
        self.save(update_fields=["status", "processed_by", "processed_at"])
    
    def __str__(self):
        return f"{self.classroom} | {self.booking_date} | ({self.start_time} | {self.end_time})"
