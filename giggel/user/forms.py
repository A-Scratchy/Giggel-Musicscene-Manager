from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_registration.forms import RegistrationForm
from .models import Profile


class updateProfileForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ('county',
                  'birth_date')
