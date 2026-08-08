from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'classroom', 'complaint_type', 'description', 'photo', 'status', 'created_at','is_deleted')
    list_filter = ('is_deleted', 'status', 'complaint_type')
    search_fields = ('name',)
    actions =['restore_complaints']
    
    def restore_complaints(self, request, queryset):
        queryset.update(is_deleted=False)
        
    restore_complaints.short_description = "Restore selected complaints"