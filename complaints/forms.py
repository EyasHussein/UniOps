from django import forms
from .models import Complaint

class ComplaintsForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'complaint_type', 
            'classroom', 
            'description', 
            'photo'
            ]

        widgets = {
            'complaint_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-cyan-500 focus:bg-white outline-none transition-all hover:border-slate-400 hover:bg-white'
            }),
            'classroom': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-cyan-500 focus:bg-white outline-none transition-all hover:border-slate-400 hover:bg-white'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-slate-100 border-2 border-slate-300 rounded-xl text-sm text-slate-900 font-medium focus:ring-0 focus:border-cyan-500 focus:bg-white outline-none transition-all resize-none min-h-[140px] hover:border-slate-400 hover:bg-white'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-bold file:bg-cyan-500 file:text-white hover:file:bg-cyan-200 transition-all'
            }),
        }