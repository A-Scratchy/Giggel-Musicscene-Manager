from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.views import LoginView


# Create your views here.


def home(request):
    return render(request, 'main/home.html', {})

class HomeNew(TemplateView, LoginView):
    template_name = 'main/home_new.html'
