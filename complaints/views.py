from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from .models import Complaint
from .forms import ComplaintsForm
from django.urls import reverse
from django.views.decorators.http import require_POST #! to make the delete and undo only to be on post

#& FOR THE UNDO NOTIFICATION
from django.middleware.csrf import get_token
from django.contrib import messages 

from django.contrib.auth.decorators import login_required

#? CREATE NEW COMPLAINT

@login_required(login_url="login")
def complaints(request: HttpRequest):
    
    #! user submitted the data
    if request.method == 'POST':
        form = ComplaintsForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False) #! Don't save to DB yet

            complaint.user = request.user   #! Link the logged-in user
            complaint.email = request.user.email

            complaint.save()                    #! Now save it
            messages.success(request, "Complaint message submitted")
            return redirect('dashboard')
    else: 
        form = ComplaintsForm()

    return render(request, 'complaints/complaints.html', {'form': form})

#? DELETE A COMPLAINT

@login_required(login_url="login")
@require_POST
def archive_complaint(request: HttpRequest, pk : int):

    complaint = get_object_or_404(Complaint, pk=pk)

    if request.user == complaint.user or request.user.role == "admin":
        ...
        #! Soft delete
        complaint.is_deleted = True
        complaint.save(update_fields=["is_deleted"])

        #! Generate the Undo URL
        undo_url = reverse('restore_complaint', args=[complaint.id])
        csrf_token = get_token(request)
        messages.success(
            request,
            f"""
            Complaint removed.
            <form method="POST" action="{undo_url}" class="inline ml-2">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <button type="submit" class="font-bold underline">
                    Undo?
                </button>
            </form>
            """,
            extra_tags='safe'
        )
    else:
        messages.error(request, "You do not have permission to delete this complaint")
        
    return redirect('dashboard')

#? UNDO DELETED COMPLAINT

@login_required(login_url="login")
@require_POST 
def restore_delete(request : HttpRequest, pk : int):
    
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.user != complaint.user and request.user.role != "admin":
        messages.error(request, "You do not have permission to restore this complaint.")
        return redirect("dashboard")
    
    complaint.is_deleted = False
    complaint.save(update_fields=["is_deleted"])
    messages.info(request, "Restored successfully.")
    return redirect('dashboard')

#? UPDATE COMPLAINT STATUS BY THE ADMIN

@login_required(login_url="login")
@require_POST
def update_complaint_status(request : HttpRequest, pk : int):
    
    if request.user.role !="admin":
        messages.error(request, "Only for Admin")
        return redirect("dashboard")
    
    complaint = get_object_or_404(Complaint, pk=pk)
    new_status = request.POST.get('new_status')

    allowed = {v for v, _ in Complaint.STATUS_CHOICES} #^ we used set {} because it's faster whith in (to check if the values in it) 

    if new_status in allowed:
        complaint.status = new_status
        complaint.save(update_fields=["status"])
        messages.success(request, f'Status for Complaint #{pk} updated to {complaint.get_status_display()}.')
    else:
        messages.error(request, "Invalid status")

    return redirect('dashboard')

#? EDIT A PENDING COMPLAINT 

@login_required(login_url="login")
def edit_complaint(request: HttpRequest, pk : int):

    complaint = get_object_or_404(Complaint, pk=pk)

    if complaint.user != request.user and request.user.role != "admin" :
        messages.error(request, "You don't have permission to edit this complaint.")
        return redirect('dashboard')

    if request.method == 'POST':

        form = ComplaintsForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes saved successfully!")
            return redirect('dashboard')

    else:
        form = ComplaintsForm(instance=complaint)

    return render(request, 'complaints/complaints.html', {
        'form': form,
        'is_edit': True,
    })


@login_required(login_url="login")
def complaint_details_partial(request: HttpRequest, pk: int):
    complaint = get_object_or_404(Complaint, pk=pk)

    
    if request.user != complaint.user and request.user.role != "admin":
        return render(request, "partials/access_denied.html", status=403)

    return render(request, "complaints/partials/complaint_details.html", {
        "complaint": complaint
    })
    
@login_required(login_url="login")
def delete_complaint(request: HttpRequest, pk : int):
    
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if request.user != complaint.user and request.user.role != "admin" :
        messages.error(request, "You don't have permission to delete this complaint.")
        return redirect("dashboard")
    
    complaint.delete()
    messages.success(request, "Complaint Deleted.")
    return redirect("dashboard")
