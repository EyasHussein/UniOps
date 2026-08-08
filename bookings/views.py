from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Booking
from .forms import BookingForm
from rooms.models import Room

#? CREATE BOOKING REQUEST
@login_required(login_url="login")
def create_booking(request : HttpRequest):

    if request.user.role != "faculty" and request.user.role != "admin":
        messages.error(request, "Only faculty can create booking requests.")
        return redirect("dashboard")
    

    selected_room = None

    if request.method == "POST":
        form = BookingForm(request.POST)
        room_id = request.POST.get("classroom")
        if room_id:
            selected_room = Room.objects.select_related("building").filter(pk=room_id).first()
            if selected_room and not selected_room.is_bookable:
                form.add_error("classroom", selected_room.non_bookable_reason)
        
        if form.is_valid():
            booking = form.save(commit=False)
            
            booking.user = request.user
            booking.email = request.user.email
            booking.status = "pending"
            try:
                booking.full_clean()
                booking.save()
                messages.success(request, "Booking request submitted successfully.")
                return redirect("dashboard")
            except ValidationError as e:
                form.add_error(None, "; ".join(e.messages))
            except Exception as e:
                form.add_error(None, f"Error: {e}")
    else:
        room_id = request.GET.get("room")
        if room_id and room_id.isdigit():
            selected_room = Room.objects.select_related("building").filter(pk=room_id).first()
            if selected_room and not selected_room.is_bookable:
                messages.error(request, selected_room.non_bookable_reason)
                selected_room = None
        initial = {"classroom": selected_room.id} if selected_room else None
        form = BookingForm(initial=initial)

    return render(
        request,
        "bookings/bookings.html",
        {
            "form": form,
            "selected_room": selected_room,
        },
    )

#? UPDATE BOOKING STATUS (ADMIN ONLY)
@login_required(login_url="login")
@require_POST
def update_booking_status(request: HttpRequest, pk: int):
    if request.user.role != "admin":
        messages.error(request, "Only admins can process bookings.")
        return redirect("dashboard")
    
    booking = get_object_or_404(Booking, pk=pk)
    action = request.POST.get('action') # legacy buttons: approved/rejected
    new_status = request.POST.get("new_status") # dropdown status update

    try:
        if new_status:
            allowed = {value for value, _ in Booking.STATUS_CHOICES}
            if new_status not in allowed:
                messages.error(request, "Invalid status.")
                return redirect("dashboard")

            if new_status == "approved":
                booking.approve(request.user)
            elif new_status == "rejected":
                booking.reject(request.user)
            else:
                booking.status = new_status
                booking.processed_by = request.user
                booking.processed_at = timezone.now()
                booking.save(update_fields=["status", "processed_by", "processed_at"])
            messages.success(request, f"Booking #{pk} status updated to {booking.get_status_display()}.")
        elif action == 'approved':
            booking.approve(request.user) # Uses your model method
            messages.success(request, f"Booking #{pk} has been approved.")
        elif action == 'rejected':
            booking.reject(request.user) # Uses your model method
            messages.success(request, f"Booking #{pk} has been rejected.")
        else:
            messages.error(request, "Invalid action.")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return redirect('dashboard')

#? EDIT BOOKING
@login_required(login_url="login")
def edit_booking(request: HttpRequest, pk: int):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.user != request.user and request.user.role != "admin":
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    if request.user.role != "admin" and booking.status != "pending":
        messages.error(request, "Only pending bookings can be edited.")
        return redirect("dashboard")

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully.")
            return redirect('dashboard')
    else:
        form = BookingForm(instance=booking)

    return render(request, 'bookings/bookings.html', {'form': form, 'is_edit': True})

#? DELETE BOOKING (SOFT DELETE)
@login_required(login_url="login")
@require_POST
def archive_booking(request: HttpRequest, pk: int):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.user != request.user and request.user.role != "admin":
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    booking.is_deleted = True
    booking.save(update_fields=["is_deleted"])

    undo_url = reverse('restore_booking', args=[booking.id])
    csrf_token = get_token(request)
    messages.success(
        request,
        f"""Booking removed. <form method="POST" action="{undo_url}" class="inline ml-2">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <button type="submit" class="font-bold underline">Undo?</button>
        </form>""",
        extra_tags='safe'
    )
    return redirect('dashboard')

#? RESTORE BOOKING
@login_required(login_url="login")
@require_POST
def restore_booking(request: HttpRequest, pk: int):
    booking = get_object_or_404(Booking, pk=pk)

    if booking.user != request.user and request.user.role != "admin":
        messages.error(request, "Permission denied.")
        return redirect("dashboard")

    booking.is_deleted = False
    booking.save(update_fields=["is_deleted"])
    messages.info(request, "Booking restored.")
    return redirect('dashboard')

#? DETAILS PARTIAL (FOR DASHBOARD MODALS)
@login_required(login_url="login")
def booking_details_partial(request: HttpRequest, pk: int):
    booking = get_object_or_404(Booking, pk=pk)
    if request.user != booking.user and request.user.role != "admin":
        return render(request, "partials/access_denied.html", status=403)
    return render(request, "bookings/partials/booking_details.html", {"booking": booking})
