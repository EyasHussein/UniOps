from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('logout/', LogoutView.as_view(next_page = ''), name = 'logout'),
]
