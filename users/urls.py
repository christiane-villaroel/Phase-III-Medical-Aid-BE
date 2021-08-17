from django import urls
from django.urls import path
from . import views
from users.forms import Patient_SignUpForm, Doctor_SignUpForm


app_name = 'users'

urlpatterns = [
   path('signup', views.patient_signup, name ='signup'),
   path('doctor-signup', views.doctor_signup, name ='doctor-signup'),
   path('login', views.login_view, name = 'login'),
   path('patient-dash', views.patient_dashboard, name = 'patient-dash'),
   path('doctor-dash', views.doctor_dashboard, name = 'doctor-dash'),

]
