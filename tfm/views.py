from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from forms import UserRegistrationForm, LoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login


def index(request):
    if request.user.is_authenticated():
        return profile(request)
    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Hash the password.
            newUser = form.instance
            print(newUser.password)
            newUser.password = make_password(newUser.password)
            newUser.username = newUser.email
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


@login_required
def profile(request):
    return render(request, 'profile.html')
