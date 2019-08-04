from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_registration.backends.activation.views import RegistrationView
from .forms import RegistrationForm, updateProfileForm
from .models import Profile
from django.core.mail import send_mail


class profile(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.profile.account_type == 'artist':
            return HttpResponseRedirect(reverse_lazy('artist_dashboard'))
        elif user.profile.account_type == 'venue':
            return HttpResponseRedirect(reverse_lazy('venue_dashboard'))
        else:
            return HttpResponseRedirect(reverse_lazy('artven'))


class updateProfile(LoginRequiredMixin, UpdateView):
    template_name = 'user/update.html'
    pslug = 'pk'
    model = Profile
    fields = ['account_type',]
    success_url = reverse_lazy('profile')


class ArtVenCreate(LoginRequiredMixin, TemplateView):
    template_name = 'user/artven.html'
