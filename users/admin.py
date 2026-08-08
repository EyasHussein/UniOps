from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
# Register your models here.
@admin.register(User)

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email','role', 'department', 'date_joined')


class UserAdmin(BaseUserAdmin):
    model = User
    
    list_display=('id', 'username', 'email', 'role', 
                    'department', 'is_staff', 'is_superuser', 'is_active'
                )
    
    list_filter = (
        'role', 'department', 'is_staff', 'is_superuser', 'is_active'
    )
    
    search_fields=('id', 'username', 'email', 'department')
    ordering = ('id',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'department')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('email', 'role', 'department')}),
    )
    