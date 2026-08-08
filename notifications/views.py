from django.shortcuts import render

# Create your views here.
def notifications(requist):
    return render(requist, 'notifications/notifications.html')