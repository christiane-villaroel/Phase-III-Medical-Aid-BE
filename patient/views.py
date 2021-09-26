from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
import datetime
from aidApp.models import Feedback, Patient, Health_Practitioner

# Create your views here.

@login_required
def support_view(request):

    user = request.user.username
    currentuser = User.objects.get(username=user)
    fullname = f"{currentuser.first_name} {currentuser.last_name}" 
    email = currentuser.email
    
    context = {
        'fullname': fullname,
        'email': email,
    }
    
    if request.method == "POST":
        if request.POST.get('fullname') and request.POST.get('message'):
            support = Feedback()
            support.fullname = request.POST.get('fullname')
            support.email = request.POST.get('email')
            support.response_type = request.POST.get('complaint')
            support.message = request.POST.get('message')
            support.save()
            send_mail(
                'Contact Support',
                'Your message has been received.  If needed, someone will follow up with you shortly.  Thank you!',
                'devops4zuri@gmail.com',
                [email],
                fail_silently=False,
                )
            return redirect('support-success')
        else: 
            messages.error(request, 'Message section can not be empty.  Submit unsuccessful.')
            return render(request, 'patient/patient-support.html', context) 
    else:
        return render(request, 'patient/patient-support.html', context)

def support_success_view(request):
    return render(request, 'patient/patient-support-feedback.html')


@login_required
def patient_dash_view(request):
    user = User.objects.get(username = request.user.username)
    patient = Patient.objects.get(patient = user)
    
    context = {
        'patient': patient
    }

    return render(request, 'patient/patient-dash.html', context)

def patient_doctor_view(request):
    
    context = {
        'doctors': Health_Practitioner.objects.all(),
        
    }
    return render(request, 'patient/patient-doctor.html', context)

def patient_profile_view(request):
    return render(request, 'patient/patient-profile.html')

def patient_clinic_view(request):
    return render(request, 'patient/patient-clinic.html')