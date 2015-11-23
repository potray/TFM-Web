from django.contrib.auth import authenticate
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django import forms
from models import Doctor, Patient
from django.contrib.auth.models import User


class UserRegistrationForm(ModelForm):
    password2 = forms.CharField(label=_("Confirm password"), widget=forms.PasswordInput)

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')

        widgets = {
            'password': forms.PasswordInput(),
            'username': forms.EmailInput(),
        }
        labels = {
            'username': 'Email',
        }
        error_messages = {
            'username': {
                'unique': _("The email already exists."),
            },
        }
        help_texts = {
            'username': "",
        }

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=50)

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Incorrect user or password")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class CreatePatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        # We exclude the sex because MaterializeCss has some problems rendering it.
        exclude = ('doctor', 'sex', 'birth_date')
