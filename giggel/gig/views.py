from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from .models import Gig, GigRequest

# Create your views here.

class GigCreate(CreateView):
    model = Gig
    template_name = 'gig/gig_create.html'
    fields = ['gig_owner', 'gig_id', 'gig_artist', 'gig_venue', 'gig_name', 'gig_date', 'gig_description']
    success_url = reverse_lazy('my_gigs')

class GigDetail(DetailView):
    model = Gig
    template_name = 'gig/gig_detail.html'
    slug_field = 'gig_id'
    context_object_name = 'gig'

class GigUpdate(LoginRequiredMixin, UpdateView):
    # need to check if user is owner of gig before allowing update
    model = Gig
    slug_field = 'gig_id'
    fields = ['gig_id', 'gig_owner', 'gig_name', 'gig_description']
    template_name = 'gig/gig_update.html'
    success_url = reverse_lazy('my_gigs')

class GigDelete(LoginRequiredMixin, DeleteView):
    model = Gig
    slug_field = 'gig_id'
    template_name = 'gig/gig_delete.html'
    success_url = reverse_lazy('profile')

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
        return Gig.objects.filter(gig_owner=self.request.user)


# Gig requests

class GigRequestCreate(CreateView):
    model = GigRequest
    template_name = 'gig/gig_request_create.html'
    fields = ['gig_request_id', 'gig_request_owner', 'gig_request_name', 'gig_request_description', 'gig_request_confimred', 'gig_request_date', 'gig_request_artist', 'gig_request_venue']
    success_url = reverse_lazy('my_gig_requests')

class GigRequestDetail(DetailView):
    model = GigRequest
    template_name = 'gig/gig_request_detail.html'
    slug_field = 'gig_request_id'
    context_object_name = 'gig_request'

class GigRequestUpdate(LoginRequiredMixin, UpdateView):
    # need to check if user is owner of gig before allowing update
    model = GigRequest
    slug_field = 'gig_request_id'
    fields = ['gig_request_id', 'gig_request_owner', 'gig_request_name', 'gig_request_description', 'gig_request_confimred', 'gig_request_date', 'gig_request_artist', 'gig_request_venue']
    template_name = 'gig/gig_request_update.html'
    success_url = reverse_lazy('my_gig_requests')

    # need to check if user is owner of gig before allowing update
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(gig_request_owner=owner)

class GigRequestDelete(LoginRequiredMixin, DeleteView):
    model = GigRequest
    slug_field = 'gig_request_id'
    template_name = 'gig/gig_request_delete.html'
    success_url = reverse_lazy('profile')

    # need to check if user is owner of gig request before allowing delete
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(gig_request_owner=owner)

class MyGigRequests(ListView):
    template_name = 'gig/my_gig_requests.html'
    context_object_name = 'gig_request'

    def get_queryset(self):
        return GigRequest.objects.filter(gig_request_owner=self.request.user)
    #OR gig requests that involve an artist or venue that they own....
