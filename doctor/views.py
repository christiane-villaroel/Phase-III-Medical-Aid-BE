from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
import datetime
from aidApp.models import Feedback, Patient, Health_Practitioner, Clinic
from .forms import HealthPractitionerForm # import form


# Create your views here.

@login_required
def doctor_dash_view(request):
    user = User.objects.get(username = request.user.username)
    doctor = Health_Practitioner.objects.get(health_practitioner = user)
    
    context = {
        'doctor': doctor
    }
    return render(request, 'doctor/doctor-dash.html', context)

def doctor_profile_view(request):
    user = User.objects.get(username = request.user.username)
    doctor = Health_Practitioner.objects.get(health_practitioner = user)
    
    context = {
        'doctor': doctor,
        
    }
    return render(request, 'doctor/doctor-profile.html', context)
    

def doctor_patient_view(request, pk):
    
    patient = get_object_or_404(Patient, id=pk)

    return render(request, 'doctor/doctor-patient.html', context={ 'patient': patient})

def doctor_consultation_view(request):
    return render(request, 'doctor/doctor-consultations.html')

def doctor_search_view(request):
    if request.method == "POST":
        search = request.POST.get('search')
        patients =Patient.objects.filter(Q(patient__first_name__icontains=search) | Q(patient__last_name__icontains=search))
    else:
        patients = Patient.objects.all()
    print()
    context = {
        'patients': patients,
        
    }
    return render(request, 'doctor/doctor-search.html', context)

def doctor_appointment_view(request):
    return render(request, 'doctor/doctor-appointment.html')

def doctor_schedule_view(request):
    today = datetime.date.today()
    month = today.month
    year = today.year
    day = today.day
    
    

    context = {
        'today': today,
        'month': month,
        'year': year,
        'day': day,
    }
    return render(request, 'doctor/doctor-schedule.html', context)
    
def doctor_schedule_week_view(request):
    return render(request, 'doctor/doctor-schedule-week.html')

@login_required
def doctor_support_view(request):

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
            return redirect('doctor-support-success')
        else: 
            messages.error(request, 'Message section can not be empty.  Submit unsuccessful.')
            return render(request, 'doctor/doctor-support.html', context) 
    else:
        return render(request, 'doctor/doctor-support.html', context)

def doctor_support_success_view(request):
    return render(request, 'doctor/doctor-support-feedback.html')

def doctor_confirm_view(request):
    return render(request, 'doctor/doctor-confirm.html')

def doctor_edit_view(request):
    user = User.objects.get(username = request.user.username)
    doctor = Health_Practitioner.objects.get(health_practitioner = user)
    instance = get_object_or_404(Health_Practitioner, health_practitioner=request.user)

    if request.method == 'POST':
        form = HealthPractitionerForm(request.POST)
        if form.is_valid():
            doctor.clinics = form.cleaned_data['clinics']
            doctor.telephone = form.cleaned_data['telephone']
            doctor.specialty = form.cleaned_data['specialty']
            doctor.consultation_times = form.cleaned_data['consultation_times']
            doctor.insurance_accepted = form.cleaned_data['insurance_accepted']
            doctor.languages = form.cleaned_data['languages']
            doctor.accepting_new_patients = form.cleaned_data['accepting_new_patients']
            doctor.save()
        else:
            print(form.errors)
    else:
        form = HealthPractitionerForm(instance=instance)

    context = {
        'doctor': doctor,
        'form': form
        
    }
    return render(request, 'doctor/doctor-edit.html', context)