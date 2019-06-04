from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_registration.forms import RegistrationForm
from django.contrib.auth.models import User
from .models import Profile


class RegistrationForm(RegistrationForm):
    county = forms.CharField(max_length=40)
    birth_date = forms.DateField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'county', 'birth_date')


class updateProfileForm(UserChangeForm):
    county = forms.CharField(max_length=40)
    birth_date = forms.DateField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'county',
                  'birth_date')
