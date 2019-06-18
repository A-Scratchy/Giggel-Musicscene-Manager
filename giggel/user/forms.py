from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_registration.forms import RegistrationForm
from .models import Profile

account_type_choices = [
    ('artist', 'Artist'),
    ('venue', 'Venue'),
    ]

class updateProfileForm(UserChangeForm):
    account_type=forms.CharField(label='Are you representing an Artist or a Venue?', widget=forms.Select(choices=account_type_choices))

    class Meta:
        model = Profile
        fields = ('county',
                  'birth_date', 'account_type')
