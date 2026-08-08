from django.urls import path
from . import views

urlpatterns = [
    path('', views.maintenance_request, name = 'maintenance'),
    
    #!delete_maintenance
    path('archive/<int:pk>/', views.archive_maintenance, name = 'archive_main'),
    
    #! restore_maintenance
    path('restore/<int:pk>/', views.restore_maintenance, name = "restore_main"),
    
    #! edit_maintenance
    path('edit/<int:pk>/', views.edit_maintenance, name= "edit_main"),
    
    #! update_maintenance_status
    path('update-status/<int:pk>/', views.update_maintenance_status, name = "update_main_status"),
    
    #! delete_maintenance
    path("delete/<int:pk>/", views.delete_maintenance, name="delete_maintenance"),
    
    #! View Popup
    path('details/<int:pk>/', views.maintenance_details_partial, name='maintenance_details_partial'),
]
