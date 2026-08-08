from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import Room, Building
from .forms import RoomForm
from bookings.models import Booking
from datetime import datetime, time, timedelta
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.contrib import messages

from django.db.models import Q, Count
# Create your views here.
HIDDEN_LECTURE_PREFIX = "[AUTO_HIDDEN_LECTURE]"

#? BUILDING LIST

@login_required(login_url="login")
def building_list(request : HttpRequest):
    q = request.GET.get("q", "").strip()
    
    buildings = (
        Building.objects
        .annotate(room_count = Count('rooms'))
        .order_by('building_type', 'name')
    )

    if q:
        buildings = buildings.filter(
            Q(name__icontains=q) |
            Q(building_type__icontains=q)
        )
        
    context = {
        'buildings' : buildings,
        'q' : q,
        'total_buildings': Building.objects.count(),
        'total_rooms': Room.objects.count(),
    }
    return render(request, 'rooms/building_list.html', context)

#? ROOM LIST

@login_required(login_url="login")
def room_list(request : HttpRequest, building_id : int):
    
    building = get_object_or_404(Building, pk=building_id)
    
    q = request.GET.get("q", "").strip()

    rooms = Room.objects.filter(building=building).order_by('room_name')
    
    if q: rooms = rooms.filter(
        Q(room_name__icontains=q) |
        Q(room_type__icontains=q) |
        Q(location__icontains=q) |
        Q(equipment__icontains=q) |
        Q(status__icontains=q) 
        )

    context = {
        #! BUILDING LIST
        'building' : building,

        #! ROOMS LIST
        'rooms' : rooms,

        #! SEARCH
        'q': q,

        #! COUNTS

        #& ROOMS
        'total_rooms' : Room.objects.filter(building=building).count(),
    }
    return render(request, 'rooms/room_list.html', context)


@login_required(login_url="login")
def room_schedule(request: HttpRequest, pk: int):
    room = get_object_or_404(Room.objects.select_related("building"), pk=pk)

    selected_date_raw = request.GET.get("date", "").strip()
    if selected_date_raw:
        try:
            selected_date = datetime.strptime(selected_date_raw, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect("room_schedule", pk=pk)
    else:
        selected_date = timezone.localdate()

    interval_raw = request.GET.get("interval", "30").strip()
    slot_minutes = 30 if interval_raw not in {"30", "60"} else int(interval_raw)

    day_bookings = list(
        Booking.objects
        .select_related("user")
        .filter(classroom=room, booking_date=selected_date, is_deleted=False)
        .exclude(status__in=["rejected", "cancelled"])
        .order_by("start_time")
    )

    day_start = datetime.combine(selected_date, time(8, 0))
    day_end = datetime.combine(selected_date, time(17, 0))
    hourly_slots = []
    maintenance_start = day_start.time()
    maintenance_end = day_end.time()
    cursor = day_start
    while cursor < day_end:
        slot_end_dt = cursor + timedelta(minutes=slot_minutes)
        slot_start = cursor.time()
        slot_end = slot_end_dt.time()

        overlapping = [
            booking for booking in day_bookings
            if booking.start_time < slot_end and booking.end_time > slot_start
        ]
        visible_overlapping = [
            booking for booking in overlapping
            if not (booking.notes and booking.notes.startswith(HIDDEN_LECTURE_PREFIX))
        ]

        if not room.is_bookable:
            slot_status = "not_bookable"
        elif room.status == "under_maintenance":
            slot_status = "maintenance"
        elif not overlapping:
            slot_status = "available"
        elif any(booking.status == "approved" for booking in overlapping):
            slot_status = "occupied"
        else:
            slot_status = "pending"

        hourly_slots.append({
            "slot_start": slot_start,
            "slot_end": slot_end,
            "status": slot_status,
            "bookings": visible_overlapping,
            "maintenance_start": maintenance_start,
            "maintenance_end": maintenance_end,
        })
        cursor = slot_end_dt

    context = {
        "room": room,
        "selected_date": selected_date,
        "selected_date_input": selected_date.isoformat(),
        "prev_date": (selected_date - timedelta(days=1)).isoformat(),
        "next_date": (selected_date + timedelta(days=1)).isoformat(),
        "hourly_slots": hourly_slots,
        "slot_minutes": slot_minutes,
        "is_room_under_maintenance": room.status == "under_maintenance",
        "is_room_bookable": room.is_bookable,
        "room_non_bookable_reason": room.non_bookable_reason,
    }
    return render(request, "rooms/room_schedule.html", context)

@login_required(login_url="login")
def add_room(request: HttpRequest):
    
    if request.user.role != "admin":
        messages.error(request, "Only admins can add rooms.")
        return redirect("rooms")
    
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            messages.success(request, "Room added successfully.")
            if room.building:
                return redirect("building_rooms", building_id=room.building.id)
            return redirect("rooms")
    else:
        form = RoomForm()
    
    return render(request, "rooms/add_room.html", {"form" : form})

@login_required(login_url="login")
def update_room(request : HttpRequest, pk : int):
    room = get_object_or_404(Room, pk=pk)
    
    if request.user.role != "admin":
        messages.error(request, 'Only admins can update rooms.')
        return redirect("rooms")

    if request.method == "POST":
        form = RoomForm(request.POST, instance= room)
        if form.is_valid():
            room = form.save()
            messages.success(request, "Room updated successfully.")
            if room.building:
                return redirect("building_rooms", building_id=room.building.id)
            return redirect("rooms")
    else:
        form = RoomForm(instance=room)
    return render(request, "rooms/add_room.html", {"form": form, 'room':room})

@login_required(login_url="login")
@require_POST
def delete_room(request :HttpRequest, pk : int):
    room = get_object_or_404(Room, pk=pk)
    
    if request.user.role != "admin":
        messages.error(request, "Only admins can delete rooms.")
        return redirect("rooms")
    if room.building :
        building_id = room.building.id
    else:
        None

    room.delete()
    messages.success(request, "the room has been deleted")
    
    if building_id:
        return redirect('building_rooms', building_id=building_id)
    return redirect("rooms")



