from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from complaints.models import Complaint
from maintenance.models import MaintenanceRequest
from bookings.models import Booking
#! for the SEARCH
from django.db.models import Q

HIDDEN_LECTURE_PREFIX = "[AUTO_HIDDEN_LECTURE]"



@login_required
def home_router(request : HttpRequest):
    if request.user.role == 'admin':
        return admin_dashboard(request)
    elif request.user.role == 'student':
        return student_dashboard(request)
    elif request.user.role == "faculty":
        return faculty_dashboard(request)
    
    messages.error(request, "Your account role is invalid.")
    return redirect("login")

#? ADMIN DASHBOARD

@login_required
def admin_dashboard(request : HttpRequest):

    if request.user.role != "admin":
        messages.error(request, "You are not allowed to access the admin dashboard.")
        return redirect("dashboard")

    #~ ACTIVE COMPLAINT
    q = request.GET.get("q", "").strip() #! for [COMPLAINTS] SEARCH
    
    active_complaints = (
        Complaint.objects
        .select_related('user', 'classroom')
        .filter(is_deleted=False)
        .order_by('user__username', '-created_at')
        ) #^ for the regroupe tage 

    #! SEARCH 
    if q:
        active_complaints = active_complaints.filter(
            Q(email__icontains=q) |
            Q(user__username__icontains=q) |
            Q(classroom__room_name__icontains=q) |
            Q(description__icontains=q) |
            Q(complaint_type__icontains=q)
            )
    
    #~ ARCHIVED_COMPLAINT
    
    archived_complaints = (
        Complaint.objects
        .select_related('user', 'classroom')
        .filter(is_deleted=True)
        .order_by('user__username', '-created_at')
        ) #^ for the regroupe tage 
    
    if q:
        archived_complaints = archived_complaints.filter(
            Q(email__icontains=q) |
            Q(user__username__icontains=q) |
            Q(classroom__room_name__icontains=q) |
            Q(description__icontains=q) |
            Q(complaint_type__icontains=q)
            )
    
    #~ ACTIVE MAINTENANCE
    mq = request.GET.get("mq", "").strip() #! for [MAINTENANCE] Search 
    
    active_main = (
        MaintenanceRequest.objects
        .select_related("user", "classroom")
        .filter(is_deleted=False)
        .order_by("user__username", "-created_at")
        )
    
    if mq:
        active_main = active_main.filter(
            Q(email__icontains=mq) |
            Q(user__username__icontains=mq) |
            Q(classroom__room_name__icontains=mq) |
            Q(description__icontains=mq) |
            Q(priority__icontains=mq) |
            Q(department__icontains=mq) |
            Q(maintenance_type__icontains=mq)
        )
        
    #~ ARCHIVED MAINTENANCE
    
    archived_main = (
        MaintenanceRequest.objects
        .select_related("user", "classroom")
        .filter(is_deleted=True)
        .order_by("user__username", "-created_at")
        )
    
    if mq:
        archived_main = archived_main.filter(
            Q(email__icontains=mq) |
            Q(user__username__icontains=mq) |
            Q(classroom__room_name__icontains=mq) |
            Q(description__icontains=mq) |
            Q(priority__icontains=mq) |
            Q(department__icontains=mq) |
            Q(maintenance_type__icontains=mq)
        )
        
        #~ ACTIVE BOOKINGS
    bq = request.GET.get("bq", "").strip() # Booking Search
    active_bookings = (
        Booking.objects
        .select_related('user', 'classroom')
        .filter(is_deleted=False)
        .exclude(notes__startswith=HIDDEN_LECTURE_PREFIX)
        .order_by('user__username', '-created_at')
    )
    
    if bq:
        active_bookings = active_bookings.filter(
            Q(user__username__icontains=bq) |
            Q(classroom__room_name__icontains=bq) |
            Q(notes__icontains=bq) |
            Q(status__icontains=bq)
        )

    #~ ARCHIVED BOOKINGS
    archived_bookings = (
        Booking.objects
        .filter(is_deleted=True)
        .exclude(notes__startswith=HIDDEN_LECTURE_PREFIX)
        .select_related('user', 'classroom')
    )
    if bq:
        archived_bookings = archived_bookings.filter(
            Q(user__username__icontains=bq) |
            Q(classroom__room_name__icontains=bq)
        )
    
    context = {
        'user_name': request.user.username,
        'email' : request.user.email,
        'is_admin' : True,
        
        #& COMPLAINTS
        'complaints' : active_complaints,
        'archived_complaints' : archived_complaints,
        'status_choices' : Complaint.STATUS_CHOICES,
        
        #&  MAINTENANCE
        'maintenance_requests' : active_main,
        'archived_main' : archived_main,
        'main_status_choices' : MaintenanceRequest.STATUS_CHOICES,
        
        #& BOOKINGS
        'bookings': active_bookings,
        'archived_bookings': archived_bookings,
        'booking_status_choices': Booking.STATUS_CHOICES,
        
        
        #! SEARCH
        'q' : q,
        'mq' : mq,
        'bq': bq,
        
        #! status / counts for Admin Cards 
        
        #& COMPLAINTS
        'total_complaints' : Complaint.objects.filter(is_deleted=False).count(),
        'pending_count': Complaint.objects.filter(is_deleted=False,status='pending').count(),
        
        #& MAINTENANCE
        'total_maintenance' : MaintenanceRequest.objects.filter(is_deleted=False).count(),
        'open_maintenance' : MaintenanceRequest.objects.filter(status="pending", is_deleted=False).count(),
    
    #& BOOKING COUNTS
        'total_bookings': Booking.objects.filter(is_deleted=False).exclude(notes__startswith=HIDDEN_LECTURE_PREFIX).count(),
        'pending_bookings_count': Booking.objects.filter(is_deleted=False, status='pending').exclude(notes__startswith=HIDDEN_LECTURE_PREFIX).count(),
    
    
    }
    
    return render(request, 'dashboards/admin_home.html', context)

#? FACULTY DASHBOARD

@login_required
def faculty_dashboard(request : HttpRequest):
    
    if request.user.role != "faculty":
        messages.error(request, "You are not allowed to access the faculty dashboard.")
        return redirect("dashboard")
    
    complaints = (
        Complaint.objects
        .select_related('user', 'classroom')
        .filter(user=request.user, is_deleted=False)
        .order_by('-created_at')
        )
    
    maintenance_requests = (
        MaintenanceRequest.objects
        .select_related('user', 'classroom')
        .filter(user=request.user, is_deleted=False)
        .order_by('-created_at')
    )
    
    bookings = (
        Booking.objects
        .select_related('user', 'classroom')
        .filter(user=request.user, is_deleted=False)
        .exclude(notes__startswith=HIDDEN_LECTURE_PREFIX)
        .order_by("-created_at")
    )
    
    context = {
        'user_name' : request.user.username,
        'is_admin' : False,
        
        #& COMPLAINTS
        'complaints' : complaints,
        
        #& MAINTENANCE
        'maintenance_requests' : maintenance_requests,
        
        #& BOOKINGS
        'bookings' : bookings,
    }
    
    return render(request, 'dashboards/faculty_home.html', context)

#? STUDENT DASHBOARD

@login_required
def student_dashboard(request : HttpRequest):
    
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access the student dashboard.")
        return redirect("dashboard")
    
    complaints = (
        Complaint.objects
        .select_related('user', 'classroom')
        .filter(user=request.user, is_deleted=False)
        .order_by('-created_at')
        )
    
    context = {
        'user_name': request.user.username,
        'is_admin' : False,
        
        #& COMPLAINTS
        'complaints': complaints,
    }
    return render(request, 'dashboards/student_home.html', context)

#? for the Notification time 

@login_required
def empty_response(request : HttpRequest):
    return HttpResponse("")
