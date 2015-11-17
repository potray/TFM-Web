from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from forms import UserRegistrationForm, LoginForm, CreatePatientForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout


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


def patients(request):
    return render(request, 'patients.html')


def create_patient(request):
    if request.method == 'POST':
        form = CreatePatientForm(request.POST)
        if (form.is_valid()):
            patient = form.instance
            # Since we excluded the sex in the form we need to get in from request.POST.
            patient.sex = request.POST['sex']
            # The patient's doctor is the user
            patient.doctor = request.user
            patient.save()
            return HttpResponseRedirect('/patients')
    else:
        form = CreatePatientForm()
    return render(request, 'create_patient.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html')
