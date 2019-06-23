from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_registration.backends.activation.views import RegistrationView
from .forms import RegistrationForm, updateProfileForm
from .models import Profile
from django.core.mail import send_mail


class profile(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'


class updateProfile(LoginRequiredMixin, UpdateView):
    template_name = 'user/update.html'
    model = Profile
    fields = ['county', 'birth_date']
    success_url = reverse_lazy('profile')


class ArtVenCreate(LoginRequiredMixin, TemplateView):
    template_name = 'user/artven.html'



