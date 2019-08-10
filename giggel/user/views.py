from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, View, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_registration.backends.activation.views import RegistrationView
from gig.models import Gig, GigRequest
from .forms import RegistrationForm, updateProfileForm
from .models import Profile
from django.core.mail import send_mail


class profile(LoginRequiredMixin, ListView):
    template_name = 'user/dashboard.html'
    login_url = reverse_lazy('login')
    model = Gig

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        owner = self.request.user
        context['gig_requests'] = GigRequest.objects.filter(gig_request_artist=self.request.user.artist)
        context['gigs'] = Gig.objects.filter(gig_artist=self.request.user.artist)
        return context

class updateProfile(LoginRequiredMixin, UpdateView):
    template_name = 'user/update.html'
    pslug = 'pk'
    model = Profile
    fields = ['account_type',]
    success_url = reverse_lazy('profile')


class ArtVenCreate(LoginRequiredMixin, TemplateView):
    template_name = 'user/artven.html'
