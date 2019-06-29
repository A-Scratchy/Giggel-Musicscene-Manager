from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from .models import Gig

# Create your views here.


class GigDetail(DetailView):
    model = Gig
    template_name = 'gig/gig_detail.html'
    slug_field = 'gig_id'
    context_object_name = 'gig'


class GigCreate(CreateView):
    model = Gig
    template_name = 'gig/gig_create.html'
    fields = ['gig_artist', 'gig_venue', 'gig_name', 'gig_date', 'gig_description']


class GigUpdate(LoginRequiredMixin, UpdateView):
    # need to check if user is owner of gig before allowing update
    model = Gig
    slug_field = 'gig_id'
    fields = ['gig_id', 'gig_owner', 'gig_name', 'gig_description']
    template_name = 'gig/gig_update.html' 
    success_url = reverse_lazy('profile')


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

