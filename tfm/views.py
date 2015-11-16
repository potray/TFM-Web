from django.http import HttpResponseRedirect
from django.shortcuts import render
from models import TfmUser
from forms import UserRegistrationForm
from  django.contrib.auth.hashers import make_password, is_password_usable, check_password



def index(request):
    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Hash the password.
            newUser = form.instance
            print(newUser.password)
            newUser.password = make_password(newUser.password)
            newUser.save()
            return HttpResponseRedirect('/')
        else:
            print ('defuq?')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})
