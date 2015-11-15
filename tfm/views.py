from django.shortcuts import render
from models import User


def index(request):
    user = User(name="asd")
    user.save()

    return render(request, 'index.html')
