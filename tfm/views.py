from random import Random
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, date
from forms import UserRegistrationForm, LoginForm, CreatePatientForm
from tfm.models import Patient, TestResult
import json


def index(request):
    if request.user.is_authenticated():
        return notifications(request)
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


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def create_patient(request):
    if request.method == 'POST':
        form = CreatePatientForm(request.POST, request.FILES)
        if form.is_valid():
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
def notifications(request):
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
    print response
    return HttpResponse(json.dumps(response))


@login_required
def patient(request):
    # Get the patient
    patient_id = request.GET['id']
    patient_object = Patient.objects.filter(id=patient_id).first()

    if request.method == 'POST':
        # The doctor changed user history
        new_history = request.POST['history']
        patient_object.description = new_history
        patient_object.save()

    # Get test results
    test_results = TestResult.objects.filter(patient=patient_object)

    return render(request, 'patient.html', {'patient': patient_object,
                                            'test_results': test_results,
                                            })


def test_result(request):
    test_id = request.GET['id']
    test = TestResult.objects.filter(id=test_id).first()

    # Since the fingers and the times aren't sorted it's necessary to do it this way.
    coordinates = ['x', 'y', 'z']
    thumb_coords = [[], [], []]
    index_coords = [[], [], []]
    middle_coords = [[], [], []]
    ring_coords = [[], [], []]
    pinky_coords = [[], [], []]

    test_json = json.loads(test.result)

    for i in range(0, test_json['times'].keys().__len__()):
        # In each iteration we add either a x, y or z coord.
        for j in range(0, coordinates.__len__()):
            # Add a "[<time>, <position in axis>]," string to each array.
            coordinate = coordinates[j]
            thumb_coords[j].append(
                '[' + test_json['times'][str(i)] + ', ' + str(float(test_json['thumb'][coordinate][str(i)]) / 10) + ']')
            index_coords[j].append(
                '[' + test_json['times'][str(i)] + ', ' + str(float(test_json['index'][coordinate][str(i)]) / 10) + ']')
            middle_coords[j].append(
                '[' + test_json['times'][str(i)] + ', ' + str(float(test_json['middle'][coordinate][str(i)]) / 10) + ']')
            ring_coords[j].append(
                '[' + test_json['times'][str(i)] + ', ' + str(float(test_json['ring'][coordinate][str(i)]) / 10) + ']')
            pinky_coords[j].append(
                '[' + test_json['times'][str(i)] + ', ' + str(float(test_json['pinky'][coordinate][str(i)]) / 10) + ']')
            if i != test_json['times'].keys().__len__():
                thumb_coords[j].append(",")
                index_coords[j].append(",")
                middle_coords[j].append(",")
                ring_coords[j].append(",")
                pinky_coords[j].append(",")

    return render(request, 'test_result.html', {'test': test,
                                                'patient': test.patient,
                                                'thumb_coords': thumb_coords,
                                                'index_coords': index_coords,
                                                'middle_coords': middle_coords,
                                                'ring_coords': ring_coords,
                                                'pinky_coords': pinky_coords, })


@csrf_exempt
def send_test_result(request):
    response = {}
    if request.method == 'POST':
        # Get the patient
        test_patient = Patient.objects.filter(id=request.POST['patient_id']).first()
        print test_patient
        print request.POST['test_type']
        print request.POST['result']
        new_result = TestResult(test_type=request.POST['test_type'], patient=test_patient,
                                result=request.POST['result'])
        new_result.save()
        response['ok'] = True
    else:
        response['ok'] = False
    return HttpResponse(json.dumps(response))
