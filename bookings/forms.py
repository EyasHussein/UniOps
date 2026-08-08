from django import forms
from .models import Booking
from django.utils import timezone

class BookingForm(forms.ModelForm):    
    class Meta:
        model = Booking
        fields = (
                    "classroom",
                    "booking_date",
                    "start_time",
                    "end_time",
                    'notes',
                )
        widgets = {
            'classroom': forms.Select(attrs={
                'class': 'w-full border bg-slate-100 border-slate-300 rounded-2xl px-4 py-3 bg-white outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500'
            }),
            'booking_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border bg-slate-100 border-slate-300 rounded-2xl px-4 py-3 outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'step': 1800,
                'min': '08:00',
                'max': '17:00',
                'class': 'w-full border bg-slate-100 border-slate-300 rounded-2xl px-4 py-3 outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'step': 1800,
                'min': '08:00',
                'max': '17:00',
                'class': 'w-full border bg-slate-100 border-slate-300 rounded-2xl px-4 py-3 outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full border bg-slate-100 border-slate-300 rounded-2xl px-4 py-3 outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["booking_date"].widget.attrs["min"] = timezone.localdate().isoformat()
        # Show only reservable spaces in the booking dropdown.
        bookable_rooms = (
            self.fields["classroom"]
            .queryset
            .select_related("building")
            .exclude(room_type="library")
            .exclude(building__building_type="cafeteria")
            .order_by("building__name", "room_name")
        )
        self.fields["classroom"].queryset = bookable_rooms
