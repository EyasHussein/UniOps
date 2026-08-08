from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'building',
            'room_name',
            'room_type',
            'capacity',
            'location',
            'status',
            'equipment'
        ]
        widgets = {
            'building': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-indigo-400 focus:bg-white outline-none transition-all hover:border-slate-400 hover:bg-white'
            }),

            'room_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-indigo-400 focus:bg-white outline-none transition-all hover:border-slate-400 hover:bg-white'
            }),

            'room_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-indigo-400 focus:bg-white outline-none transition-all hover:border-slate-400 hover:bg-white'
            }),

            'capacity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-indigo-400 focus:bg-white outline-none transition-all hover:border-slate-400 hover:bg-white'
            }),

            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-indigo-400 focus:bg-white outline-none transition-all hover:border-slate-400 hover:bg-white'
            }),

            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-indigo-400 focus:bg-white outline-none transition-all hover:border-slate-400 hover:bg-white'
            }),

            'equipment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-indigo-400 focus:bg-white outline-none transition-all resize-none min-h-[140px] hover:border-slate-400 hover:bg-white'
            }),
        }