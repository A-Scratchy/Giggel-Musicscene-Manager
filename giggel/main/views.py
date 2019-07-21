from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.


def home(request):
    return render(request, 'main/home.html', {})

class HomeNew(TemplateView):
    template_name = 'main/home_new.html'
