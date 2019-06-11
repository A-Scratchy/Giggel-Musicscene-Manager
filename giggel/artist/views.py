from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, TemplateView
from .models import Artist


# Create your views here.


class ArtistDetail(DetailView):
    model = Artist
    template_name = 'artist/artist_detail.html'
    slug_field = 'artist_id'


class ArtistDashboard(LoginRequiredMixin, TemplateView):
    model = Artist
    template_name = 'artist/artist_dashboard.html'
    login_url = reverse_lazy('login')


class ArtistCreate(CreateView):
    model = Artist
    fields = ['artist_id', 'artist_owner', 'artist_name', 'artist_description']
    template_name = 'artist/artist_create.html'
    success_url = reverse_lazy('profile')
    # form_class = ContactForm


class ArtistUpdate(UpdateView):
    model = Artist
    template_name = 'artist/Artist_update.html'


class ArtistDelte(DeleteView):
    model = Artist
    template_name = 'artist/Artist_delete.html'
