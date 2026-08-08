from django.shortcuts import render, redirect, get_object_or_404
from .forms import MaintenanceForm
from .models import MaintenanceRequest
from django.contrib import messages

from django.http import HttpRequest

from django.middleware.csrf import get_token

from django.urls import reverse

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

#? CREATE MAINTENANCE REQUEST

@login_required(login_url="login")
def maintenance_request(request : HttpRequest):

    if request.user.role != 'faculty' and request.user.role != "admin":
        messages.error(request, "Only faculty can submit maintenance requests.")
        return redirect("dashboard")

    if request.method == "POST":
        form = MaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            main = form.save(commit=False)
            main.user = request.user
            main.email = request.user.email
            main.department = request.user.department
            main.save()
            messages.success(request, "Mantenance request submitted.")
            return redirect("dashboard")
    else:
        form = MaintenanceForm()
    return render(request, "maintenance/maintenance.html", {'form' : form})


#? ARCHIVE (DELETE) MAINTENANCE

@login_required(login_url="login")
@require_POST
def archive_maintenance(request : HttpRequest, pk : int):
    main = get_object_or_404(MaintenanceRequest, pk=pk)
    
    if main.user != request.user and request.user.role != "admin":
        messages.error(request, "You don't have permission to archive this Maintenance request")
        return redirect("dashboard")

    main.is_deleted = True
    main.save()

    undo_url = reverse('restore_main', args=[main.id])
    csrf_token = get_token(request)
    messages.success(
        request, 
        f'''
            Maintenance archived. 
            <form method="POST" action="{undo_url}" class="inline" >
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <button type="submit" class='font-bold underline'>
                    Undo?
                </button>
            </form>
        ''',
            extra_tags='safe'
    )

    return redirect("dashboard")

#? RESTORE (UNDO DELETE) MAINTENANCE

@login_required(login_url="login")
@require_POST
def restore_maintenance(request : HttpRequest, pk : int):
    main = get_object_or_404(MaintenanceRequest, pk=pk)
    
    if request.user.role != "admin":
        messages.error(request, "You don't have permission to restore this Maintenance request")
        return redirect("dashboard")

    main.is_deleted = False
    main.save()
    messages.info(request, "Maintenance request restored.")
    return redirect("dashboard")

#? UPDATE A PENDING MAINTENANCE

@login_required(login_url="login")
def edit_maintenance(request : HttpRequest, pk : int):
    
    main = get_object_or_404(MaintenanceRequest, pk=pk)
    
    if main.user != request.user and request.user.role != "admin":
        messages.error(request, "You don't have permission to edit this Maintenance request")
        return redirect("dashboard")
    
    if request.method == "POST":
        form = MaintenanceForm(request.POST, request.FILES, instance=main)
        if form.is_valid():
            form.save()
            messages.success(request, "Maintenance request updated.")
            return redirect("dashboard")
    else:
        form = MaintenanceForm(instance=main)
    
    context = {
        "form" : form,
        "is_edit" : True, 
    }
    return render(request, "maintenance/maintenance.html", context)

#? UPDATE MAINTENANCE STATUS BY THE ADMIN

@login_required(login_url="login")
@require_POST
def update_maintenance_status(request : HttpRequest, pk : int):
    main = get_object_or_404(MaintenanceRequest, pk=pk)
    
    if request.user.role != "admin":
        messages.error(request, "Admins only")
        return redirect("dashboard")

    new_status = request.POST.get("new_status")

    allowed = {v for v,_ in MaintenanceRequest.STATUS_CHOICES}
    if new_status not in allowed:
        messages.error(request, "Invalid status")
        return redirect("dashboard")

    main.status = new_status
    main.save(update_fields=["status"])
    messages.success(request, f"Status Maintenance for #{pk} updated to {main.get_status_display()}.")
    return redirect("dashboard")

@login_required(login_url="login")
def maintenance_details_partial(request: HttpRequest, pk: int):
    main = get_object_or_404(MaintenanceRequest, pk=pk)

    
    if request.user != main.user and request.user.role != "admin":
        return render(request, "partials/access_denied.html", status=403)

    return render(request, "maintenance/partials/maintenance_details.html", {
        "main": main
    })
    

def delete_maintenance(request : HttpRequest, pk : int):
    main = get_object_or_404(MaintenanceRequest, pk=pk)
    
    if request.user != main.user and request.user.role != "admin":
        messages.error(request, "You don't have permission to delete this Maintenance request")
        return redirect("dashboard")
    
    main.delete()
    messages.success(request, "Maintenance Deleted.")
    main.save()
    return redirect("dashboard")