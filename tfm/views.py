from random import Random
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, date
from forms import UserRegistrationForm, LoginForm, CreatePatientForm, PatientSettingsForm
from tfm.models import Patient, TestResult, PatientSettings
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
                return HttpResponseRedirect('/notifications')
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
    attrs = {}
    if request.method == 'POST':
        form = CreatePatientForm(request.POST, request.FILES)
        if form.is_valid():

            if request.POST.get('update') is not None:
                # Editing
                previous_patient = Patient.objects.filter(id=request.POST['update']).first()
                previous_patient.first_name = request.POST['first_name']
                previous_patient.last_name = request.POST['last_name']
                previous_patient.history = request.POST['history']

                if request.POST['sex'] == 'M':
                    previous_patient.sex = True
                else:
                    previous_patient.sex = False

                date_string = request.POST['birth_date']
                try:
                    day = int(date_string[0:2])
                    month = int(date_string[3:5])
                    year = int(date_string[6:10])
                    birth_date = date(year, month, day)
                    previous_patient.birth_date = birth_date
                except:
                    # Date didn't change.
                    previous_patient.birth_date = previous_patient.birth_date

                if request.FILES.get('photo') is not None:
                    # Change the photo
                    previous_patient.photo = request.FILES.get('photo')

                previous_patient.save()
            else:
                patient = form.instance
                # Since we excluded the sex in the form we need to get in from request.POST.
                if request.POST['sex'] == 'M':
                    patient.sex = True
                else:
                    patient.sex = False
                # The patient's doctor is the user
                patient.doctor = request.user
                # Create default settings
                settings = PatientSettings()
                settings.save()
                patient.settings = settings
                # Create a date from the form info
                date_string = request.POST['birth_date']
                print date_string
                day = int(date_string[0:2])
                month = int(date_string[3:5])
                year = int(date_string[6:10])
                birth_date = date(year, month, day)
                patient.birth_date = birth_date

                patient.save()
            return HttpResponseRedirect('/patients')
    else:
        form = CreatePatientForm()
        if request.GET.get('id') is not None:
            # Edit patient.
            patient = Patient.objects.filter(id=request.GET['id']).first()
            attrs['patient'] = patient
            # Prefill the text fields.
            form.fields['first_name'].initial = patient.first_name
            form.fields['last_name'].initial = patient.last_name
            form.fields['history'].initial = patient.history
    attrs['form'] = form
    return render(request, 'create_patient.html', attrs)


@login_required
def patient_settings(request):
    # Get patient
    patient = Patient.objects.filter(id=request.GET['id']).first()
    if request.method == 'POST':
        # Get sent data and save the settings.
        form = PatientSettingsForm(request.POST)
        if form.is_valid():
            settings = form.instance
            print settings.diary_straight_line
            previous_settings = patient.settings
            previous_settings.delete()
            settings.save()
            patient.settings = settings
            patient.save()

    render_form = PatientSettingsForm()

    # Prefill the fields
    settings = patient.settings
    render_form.fields['diary_straight_line'].initial = settings.diary_straight_line
    render_form.fields['diary_simon_says_hand'].initial = settings.diary_simon_says_hand
    render_form.fields['diary_simon_says_tool'].initial = settings.diary_simon_says_tool
    render_form.fields['simon_says_hand_max_hooks'].initial = settings.simon_says_hand_max_hooks
    render_form.fields['simon_says_tool_max_hooks'].initial = settings.simon_says_tool_max_hooks

    return render(request, 'patient_settings.html', {'patient': patient,
                                                     'form': render_form})

@login_required
def list_patients(request):
    if request.method == 'POST':
        # The doctor deleted a patient
        patient = Patient.objects.filter(id=request.POST['patient_id']).first()
        patient.delete()

    doctor_patients = Patient.objects.filter(doctor=request.user).order_by('last_name')

    for patient in doctor_patients:
        patient.code = str(patient.id).zfill(6)

    return render(request, 'patients.html', {'patients': doctor_patients})


@login_required
def notifications(request):
    # Get all unread notifications.
    unread_notifications = TestResult.objects.filter(is_new=True)

    # Filter by doctor.
    filtered_notifications = []
    for notification in unread_notifications:
        if notification.patient.doctor == request.user:
            filtered_notifications.append(notification)

    return render(request, 'notifications.html', {'notifications': filtered_notifications})


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
        response['diary_straight_line'] = patient[0].settings.diary_straight_line
        response['diary_simon_says_hand'] = patient[0].settings.diary_simon_says_hand
        response['diary_simon_says_tool'] = patient[0].settings.diary_simon_says_tool
        response['simon_says_hand_max_hooks'] = patient[0].settings.simon_says_hand_max_hooks
        response['simon_says_tool_max_hooks'] = patient[0].settings.simon_says_tool_max_hooks
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
    test_results = TestResult.objects.filter(patient=patient_object).order_by('-date')

    return render(request, 'patient.html', {'patient': patient_object,
                                            'test_results': test_results,
                                            })


@login_required
def test_result(request):
    test_id = request.GET['id']
    test = TestResult.objects.filter(id=test_id).first()

    # If the doctor acceded it then it isn't new.
    if test.is_new:
        test.is_new = False
        test.save()


    if (test.test_type == 'SS'):

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
                    '[' + test_json['times'][str(i)] + ', ' + str(
                        float(test_json['middle'][coordinate][str(i)]) / 10) + ']')
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

        touch_times = []
        for i in range(0, test_json['touchTimes'].keys().__len__()):
            touch_times.append(test_json['touchTimes'][str(i)])

        return render(request, 'test_result.html', {'test': test,
                                                    'patient': test.patient,
                                                    'thumb_coords': thumb_coords,
                                                    'index_coords': index_coords,
                                                    'middle_coords': middle_coords,
                                                    'ring_coords': ring_coords,
                                                    'pinky_coords': pinky_coords,
                                                    'touch_times': touch_times,})
    elif test.test_type == 'SL':
        coordinates = ['x', 'y', 'z']
        index_coords = [[], [], []]

        test_json = json.loads(test.result)

        for i in range(0, test_json['times'].keys().__len__()):
            # In each iteration we add either a x, y or z coord.
            for j in range(0, coordinates.__len__()):
                # Add a "[<time>, <position in axis>]," string to each array.
                coordinate = coordinates[j]
                index_coords[j].append(
                    '[' + test_json['times'][str(i)] + ', ' + str(float(test_json['index'][coordinate][str(i)]) / 10) + ']')

                if i != test_json['times'].keys().__len__():
                    index_coords[j].append(",")


        return render(request, 'test_result.html', {
            'test': test,
            'patient': test.patient,
            'index_coords': index_coords,
        })

    elif test.test_type == 'ST':
        coordinates = ['x', 'y', 'z']
        tool_coords = [[], [], []]

        test_json = json.loads(test.result)
        for i in range(0, test_json['times'].keys().__len__()):
            # In each iteration we add either a x, y or z coord.
            for j in range(0, coordinates.__len__()):
                # Add a "[<time>, <position in axis>]," string to each array.
                coordinate = coordinates[j]
                tool_coords[j].append(
                    '[' + test_json['times'][str(i)] + ', ' + str(float(test_json['tool'][coordinate][str(i)]) / 10) + ']')

                if i != test_json['times'].keys().__len__():
                    tool_coords[j].append(",")

        touch_times = []
        for i in range(0, test_json['touchTimes'].keys().__len__()):
            touch_times.append(test_json['touchTimes'][str(i)])

        return render(request, 'test_result.html', {
            'test': test,
            'patient': test.patient,
            'tool_coords': tool_coords,
            'touch_times': touch_times,
        })




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
