from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegistrationForm, updateProfileForm
from .models import Profile
from django.core.mail import send_mail


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
                request, f'Thanks {username}! Your account has been updated.')
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

# used to test email settings. Sends a one off email


def testEmail(request):
    # user = User.objects.create_user(
    #     username='Mr Test11', password='AB12345', email='ascratcherd@brake.org.uk')
    subject = 'test'
    message = 'some new message'
    from_email = settings.DEFAULT_FROM_EMAIL
    # user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
    email = user.email
    # send_mail(subject, message, from_email, [email], fail_silently=False,)
    return HttpResponse('<html>' + settings.DEFAULT_FROM_EMAIL + '</html>')
