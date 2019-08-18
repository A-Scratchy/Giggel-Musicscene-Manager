from django.urls import reverse_lazy, reverse
from django_filters.views import FilterView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView, View
from django.http import HttpResponse, HttpResponseRedirect
from .models import Gig, GigRequest, GigRequestForm, GigForm
from venue.models import Venue
from artist.models import Artist
from django.core.paginator import Paginator
import random
import string

# Create your views here.

class GigCreate(SuccessMessageMixin, CreateView):
    model = Gig
    template_name = 'gig/gig_create.html'
    form_class = GigForm
    success_url = reverse_lazy('my_gigs')
    success_message = 'Gig was created successfully'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.gig_owner = self.request.user
        self.object.gig_id= "".join(
                [random.choice(string.digits +
                               string.ascii_letters) for i in range(20)]
                )
        # check if user has artist or venue
        if self.request.user.profile.account_type == 'artist':
            self.object.gig_artist = self.request.user.artist
        elif self.request.user.profile.account_type == 'venue':
            self.object.gig_venue = self.request.user.venue
        else:
            messages.warning(self.request, 'account has no artist or venue')
            return HttpResponseRedirect(self.success_url)
        self.object.save()
        success_message = super().get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return HttpResponseRedirect(self.success_url)

class GigDetail(DetailView):
    model = Gig
    template_name = 'gig/gig_detail.html'
    slug_field = 'gig_id'
    context_object_name = 'gig'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        owner = self.request.user
        context['gigs'] = Gig.objects.all()
        paginator = Paginator(context['gigs'], 8) # Show 25 gigs per page
        page = self.request.GET.get('page')
        context['pag_gigs'] = paginator.get_page(page)
        return context

class GigUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    # need to check if user is owner of gig before allowing update
    model = Gig
    slug_field = 'gig_id'
    form_class = GigForm
    template_name = 'gig/gig_update.html'
    success_url = reverse_lazy('my_gigs')
    success_message = 'Gig was updated successfully'

class GigDelete(LoginRequiredMixin, DeleteView):
    model = Gig
    slug_field = 'gig_id'
    template_name = 'gig/gig_delete.html'
    success_url = reverse_lazy('my_gigs')

    def post(self, request, *args, **kwargs):
        messages.warning(request, 'Gig has been deleted')
        return super().post(self, request, *args, **kwargs)

    # need to check if user is owner of gig before allowing update
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(gig_owner=owner)


class GigDirectory(FilterView):
    model = Gig
    template_name = 'gig/gig_directory.html'

class MyGigs(ListView):
    template_name = 'gig/my_gigs.html'

    def get_queryset(self):
        try:
            self.request.user.artist
            return Gig.objects.filter(gig_artist=self.request.user.artist)
        except Artist.DoesNotExist:
            try:
                 self.request.user.venue
                 return Gig.objects.filter(gig_venue=self.request.user.venue)
            except Venue.DoesNotExist:
                messages.add_message(self.request, messages.WARNING, 'You will need to create and artist or venue first')
                return []


# Gig requests

class GigRequestCreate(SuccessMessageMixin, CreateView):
    model = GigRequest
    template_name = 'gig/gig_request_create.html'
    success_url = reverse_lazy('profile')
    success_message = "Gig request was created successfully"
    form_class = GigRequestForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.gig_request_id= "".join(
                [random.choice(string.digits +
                               string.ascii_letters) for i in range(20)]
                )
        owner = self.request.user
        self.object.gig_request_owner = owner
        # check if user has artist or venue
        if self.request.user.profile.account_type == 'artist':
            self.object.gig_request_artist = self.request.user.artist
            self.object.gig_request_venue = Venue.objects.get(venue_id=self.request.GET['gig_request_venue'])
        elif self.request.user.profile.account_type == 'venue':
            self.object.gig_request_venue = self.request.user.venue
            self.object.gig_request_artist = Artist.objects.get(artist_id=self.request.GET['gig_request_artist'])
        else:
            messages.warning(self.request, 'account has no artist or venue')
            return HttpResponseRedirect(self.success_url)
        self.object.save()
        success_message = super().get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return HttpResponseRedirect(self.success_url)

class GigRequestDetail(DetailView):
    model = GigRequest
    template_name = 'gig/gig_request_detail.html'
    slug_field = 'gig_request_id'
    context_object_name = 'gig_request'

class GigRequestUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    # need to check if user is owner of gig before allowing update
    model = GigRequest
    slug_field = 'gig_request_id'
    form_class = GigRequestForm
    template_name = 'gig/gig_request_update.html'
    success_url = reverse_lazy('profile')
    success_message = "gig request was updated successfully"

    # need to check if user is owner of gig before allowing update
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(gig_request_owner=owner)

class GigRequestDelete(LoginRequiredMixin, DeleteView):
    model = GigRequest
    slug_field = 'gig_request_id'
    template_name = 'gig/gig_request_delete.html'
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        messages.warning(request, 'Requset has been deleted')
        return super().post(self, request, *args, **kwargs)

    # need to check if user is owner of gig request before allowing delete
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(gig_request_owner=owner)

class MyGigRequests(ListView):
    template_name = 'gig/my_gig_requests.html'
    context_object_name = 'gig_request'

    def get_queryset(self):
        try:
            self.request.user.artist
            return GigRequest.objects.filter(gig_request_artist=request.user.artist)
        except Artist.DoesNotExist:
            try:
                 self.request.user.venue
                 return GigRequest.objects.filter(gig_request_venue=request.user.venue)
            except Venue.DoesNotExist:
                messages.add_message(self.request, messages.WARNING, 'You will need to create and artist or venue first')
                return []
    #OR gig requests that involve an artist or venue that they own....

class GigRequestConfirm(DetailView):
    model = GigRequest
    slug_field = 'gig_request_id'
    form_class = GigRequestForm
    template_name = 'gig/gig_request_update.html'
    success_url = reverse_lazy('profile')
    success_message = "gig request was updated successfully"

    def get(self, request, *args, **kwargs):
        gig_request = self.get_object()
        gig = Gig.objects.create(
    gig_owner = gig_request.gig_request_owner,
    gig_id = "".join(
            [random.choice(string.digits +
                           string.ascii_letters) for i in range(20)]
            ),
    gig_artist = gig_request.gig_request_artist,
    gig_venue = gig_request.gig_request_venue,
    gig_date = gig_request.gig_request_date,
    gig_description = gig_request.gig_request_description
        )
        gig_request.confirm()
        gig_request.save()
        messages.warning(request, gig_request.gig_request_confirmed)
        return HttpResponseRedirect(self.success_url)
