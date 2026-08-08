from django.urls import path
from . import views

urlpatterns = [
    path('', views.complaints, name='complaints'),
    
    #! Path for the archive action
    path('archive/<int:pk>/', views.archive_complaint, name='archive_complaint'),
    
    #! path for the restore action
    path('restore/<int:pk>/', views.restore_delete, name='restore_complaint'),
    
    #! path to Update compalint status
    path('update-status/<int:pk>/', views.update_complaint_status, name='update_complaint_status'),
    
    #! path to Update (Edit) the whole compalint
    path('edit/<int:pk>/', views.edit_complaint, name='edit_complaint'),
    
    #! path to Delete actions
    path("delete/<int:pk>/", views.delete_complaint, name="delete_complaint"),
    
    #! path for popup view 
    path('details/<int:pk>/', views.complaint_details_partial, name='complaint_details_partial'),
]

#? the int to pick just numbers (because id's are numbers) any thing else is an error

