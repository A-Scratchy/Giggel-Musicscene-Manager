from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'main/home.html', {})

# blank page used for testing


def blankPage(request):
    return HttpResponse('<html>a blank page</html>')
