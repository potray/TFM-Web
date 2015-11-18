from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta, date
from forms import UserRegistrationForm, LoginForm, CreatePatientForm
from tfm.models import Patient


def index(request):
    if request.user.is_authenticated():
        return profile(request)
    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Hash the password.
            print form.cleaned_data
            newUser = form.instance
            newUser.password = make_password(newUser.password)
            newUser.email = newUser.username
            newUser.save()
            return HttpResponseRedirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return HttpResponseRedirect('/profile')
            else:
                print"no"
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def create_patient(request):
    if request.method == 'POST':
        form = CreatePatientForm(request.POST)
        if (form.is_valid()):
            patient = form.instance
            # Since we excluded the sex in the form we need to get in from request.POST.
            patient.sex = request.POST['sex']
            # The patient's doctor is the user
            patient.doctor = request.user
            # Create a date from the form info
            date_string = request.POST['birth_date']
            day = int(date_string[0:2])
            month = int(date_string[3:5])
            year = int(date_string[6:10])
            birth_date = date(year, month, day)
            patient.birth_date = birth_date
            patient.save()
            return HttpResponseRedirect('/patients')
    else:
        form = CreatePatientForm()
    return render(request, 'create_patient.html', {'form': form})


@login_required
def list_patients(request):
    doctor_patients = Patient.objects.filter(doctor=request.user).order_by('last_name')

    for patient in doctor_patients:
        patient.code = str(patient.id).zfill(6)

    return render(request, 'patients.html', {'patients': doctor_patients})


@login_required
def profile(request):
    return render(request, 'profile.html')

def crossdomain(request):
    return HttpResponse(open('crossdomain.xml').read())


def validate_patient_code(request):
    # Take off the zeros to the left.
    code = int(request.GET['code'])
    patient = Patient.objects.filter(id=code)
    response = {}
    if patient:
        response['first_name'] = patient[0].first_name
        response['last_name'] = patient[0].last_name
        response['ok'] = True
    else:
        response['ok'] = False
    return HttpResponse(response)
