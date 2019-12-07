from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.views import LoginView


# Create your views here.

class Home(TemplateView):
    template_name = 'main/home.html'

class HomeNew(TemplateView, LoginView):
    template_name = 'main/home_new.html'
