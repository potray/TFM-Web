from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django import forms
from models import TfmUser


class UserRegistrationForm(ModelForm):
    # name = forms.CharField(label='Name', max_length=100)
    # surname = forms.CharField(label='Surname', max_length=200)
    # user_name = forms.CharField(label='User Name', max_length=50)
    # user_password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=50)
    class Meta:
        model = TfmUser
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }
        error_messages = {
            'email': {
                'unique': _("The email already exists."),
            },
        }
