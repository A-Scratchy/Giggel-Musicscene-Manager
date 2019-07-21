from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView, View
from django.http import HttpResponse, HttpResponseRedirect
from .models import Gig, GigRequest
from venue.models import Venue
from artist.models import Artist
import random
import string

# Create your views here.

class GigCreate(SuccessMessageMixin, CreateView):
    model = Gig
    template_name = 'gig/gig_create.html'
    fields = ['gig_owner', 'gig_id', 'gig_artist', 'gig_venue', 'gig_name', 'gig_date', 'gig_description']
    success_url = reverse_lazy('my_gigs')
    success_message = '%(gig_name)s was created successfully'

class GigDetail(DetailView):
    model = Gig
    template_name = 'gig/gig_detail.html'
    slug_field = 'gig_id'
    context_object_name = 'gig'

class GigUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    # need to check if user is owner of gig before allowing update
    model = Gig
    slug_field = 'gig_id'
    fields = ['gig_id', 'gig_owner', 'gig_name', 'gig_description']
    template_name = 'gig/gig_update.html'
    success_url = reverse_lazy('my_gigs')
    success_message = '%(gig_name)s was updated successfully'

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


class GigDirectory(ListView):
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
                return HttpResponseRedirect(reverse_lazy('artven'))


# Gig requests

class GigRequestAtVenueCreate(SuccessMessageMixin, CreateView):
    model = GigRequest
    template_name = 'gig/gig_request_create.html'
    fields = ['gig_request_name', 'gig_request_description', 'gig_request_date']
    success_url = reverse_lazy('artist_dashboard')
    success_message = "%(gig_request_name)s was created successfully"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.gig_request_id= "".join(
                [random.choice(string.digits +
                               string.ascii_letters) for i in range(20)]
                )
        self.object.gig_request_owner = self.request.user
        self.object.gig_request_artist = self.request.user.artist
        self.object.gig_request_venue = Venue.objects.get(venue_id=self.request.GET['gig_request_venue'])
        self.object.save()
        success_message = super().get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return HttpResponseRedirect(self.success_url)

class GigRequestToArtistCreate(SuccessMessageMixin, CreateView):
    model = GigRequest
    template_name = 'gig/gig_request_create.html'
    fields = ['gig_request_name', 'gig_request_description', 'gig_request_date']
    success_url = reverse_lazy('venue_dashboard')
    success_message = "%(gig_request_name)s was created successfully"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.gig_request_id= "".join(
                [random.choice(string.digits +
                               string.ascii_letters) for i in range(20)]
                )
        self.object.gig_request_owner = self.request.user
        self.object.gig_request_venue = self.request.user.venue
        self.object.gig_request_artist = Artist.objects.get(artist_id=self.request.GET['gig_request_artist'])
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
    fields = ['gig_request_id', 'gig_request_owner', 'gig_request_name', 'gig_request_description', 'gig_request_confirmed', 'gig_request_date', 'gig_request_artist', 'gig_request_venue']
    template_name = 'gig/gig_request_update.html'
    success_url = reverse_lazy('profile')
    success_message = "%(gig_request_name)s was updated successfully"

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
            request.user.artist
            return GigRequest.objects.filter(gig_request_artist=request.user.artist)
        except Artist.DoesNotExist:
            try:
                 request.user.venue
                 return GigRequest.objects.filter(gig_request_venue=request.user.venue)
            except Venue.DoesNotExist:
                messages.add_message(self.request, messages.WARNING, 'You will need to create and artist or venue first')
                return HttpResponseRedirect(reverse_lazy('artven'))
    #OR gig requests that involve an artist or venue that they own....

class GigRequestConfirm(DetailView):
    model = GigRequest
    slug_field = 'gig_request_id'
    fields = ['gig_request_id', 'gig_request_owner', 'gig_request_name', 'gig_request_description', 'gig_request_confirmed', 'gig_request_date', 'gig_request_artist', 'gig_request_venue']
    template_name = 'gig/gig_request_update.html'
    success_url = reverse_lazy('profile')
    success_message = "%(gig_request_name)s was updated successfully"

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
    gig_name = gig_request.gig_request_name,
    gig_date = gig_request.gig_request_date,
    gig_description = gig_request.gig_request_description
        )
        gig_request.confirm()
        gig_request.save()
        messages.warning(request, gig_request.gig_request_confirmed)
        return HttpResponseRedirect(self.success_url)
