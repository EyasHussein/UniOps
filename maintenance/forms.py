from django import forms
from .models import MaintenanceRequest

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['maintenance_type', 'classroom', 'priority', 'description', 'photo']
        widgets = {
            'maintenance_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-amber-400 focus:bg-white outline-none transition-all hover:border-slate-400 hover:bg-white'
            }),
            'classroom': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-amber-400 focus:bg-white outline-none transition-all hover:border-slate-400 hover:bg-white'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-amber-400 focus:bg-white outline-none transition-all hover:border-slate-400 hover:bg-white'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-amber-400 focus:bg-white outline-none transition-all resize-none min-h-[140px] hover:border-slate-400 hover:bg-white'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-bold file:bg-amber-100 file:text-amber-700 hover:file:bg-amber-200 transition-all'
            }),
        }