from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django_registration.backends.activation.views import RegistrationView
from .forms import RegistrationForm, updateProfileForm
from .models import Profile
from django.core.mail import send_mail


@login_required
def profile(request):
    return render(request, 'user/profile.html', {})


@login_required
def updateProfile(request):
    if request.method == 'POST':
        form = updateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.county = form.cleaned_data.get('county')
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            username = form.cleaned_data.get('username')
            user.save()
            messages.success(
                request, f'Thanks { user.username }! Your account has been updated.')
            return redirect('profile')
        else:
            messages.warning(
                request, 'We\'re sorry, your form contains errors. Please fix and try again.')
            return redirect('updateProfile')
    else:
        user = request.user
        data = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
                'email': user.email, 'county': user.profile.county, 'birth_date': user.profile.birth_date}
        form = updateProfileForm(initial=data)
    return render(request, 'user/update.html', {'form': form})
