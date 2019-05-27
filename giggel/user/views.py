from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.county = form.cleaned_data.get('county')
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, f'Thanks {username}! Your account is now set up.')
            return redirect('profile')
        else:
            messages.warning(
                request, 'We\'re sorry, your form contains errors. Please fix and try again.')
            return redirect('register')
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'user/profile.html', {})


@login_required
def updateProfile(request):
    return render(request, 'user/profile.html', {})
