"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from . import views

from django.conf import settings
from django.conf.urls.static import static



# from rooms import views as room_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.home_router, name='dashboard'),
    
    #! for message time
    path('empty-response/', views.empty_response, name = "empty_response"),
    
    #! inclouds
    path('', include('users.urls')),
    path('bookings/', include('bookings.urls')),
    path('complaints/', include('complaints.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('notifications/', include('notifications.urls')),
    path('rooms/', include('rooms.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


