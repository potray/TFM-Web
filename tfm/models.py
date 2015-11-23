from django.contrib.auth.models import User
from django.db import models


# class TfmUser(models.Model):
#     user = models.OneToOneField(User)
#     # name = models.CharField(max_length=100, null=False)
#     # surname = models.CharField(max_length=200, null=False)
#     # email = models.EmailField(max_length=100, unique=True, primary_key=True, null=False)
#     # password = models.CharField(max_length=50, null=False)

class Doctor(models.Model):
    specialization = models.CharField(max_length=100)


class Patient(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    first_name = models.CharField(max_length=100, null=False, default='')
    last_name = models.CharField(max_length=200, null=False, default='')
    description = models.TextField()
    sex = models.BooleanField(max_length=1, choices=SEX_CHOICES)
    doctor = models.ForeignKey(User)
    birth_date = models.DateField()
    photo = models.ImageField(upload_to='photos')


class TestResult(models.Model):
    SIMON_SAYS = "SS"
    STRAIGHT_LINE = "SL"
    TEST_CHOICES = (
        (SIMON_SAYS, 'Simon says'),
        (STRAIGHT_LINE, "Straight line"),
    )
    test_type = models.CharField(max_length=2, choices=TEST_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient)
    result = models.TextField()
    is_new = models.BooleanField(default=True)
