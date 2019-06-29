from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, TemplateView, View, ListView
from django.http import HttpResponse, HttpResponseRedirect
from .models import Artist

# Create your views here.


class ArtistDetail(DetailView):
    model = Artist
    template_name = 'artist/artist_detail.html'
    slug_field = 'artist_id'
    context_object_name = 'artist'


class ArtistDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'artist/artist_dashboard.html'
    login_url = reverse_lazy('login')


class ArtistCreate(View):
    def get(self, request):
        user = request.user
        try:
            user.artist
            messages.add_message(self.request, messages.WARNING, 'you already have an artist')
        except Artist.DoesNotExist:
            artist_id = 'art' + user.username
            user.artist = Artist.objects.create(artist_owner=user, artist_name="", artist_id=artist_id)
            # consider changing this auto slug to a randomised number/string to make it hard to guess
            user.profile.account_type = 'artist'
            user.save()
            return HttpResponseRedirect(reverse_lazy('artist_update', kwargs={'slug':artist_id}))
        else:
            return HttpResponseRedirect(reverse_lazy('artist_dashboard'))


class ArtistUpdate(LoginRequiredMixin, UpdateView):
    # need to check if user is owner of artist before allowing update
    model = Artist
    slug_field = 'artist_id'
    fields = ['artist_id', 'artist_owner', 'artist_name', 'artist_description']
    template_name = 'artist/artist_update.html' 
    success_url = reverse_lazy('artist_dashboard')


class ArtistDelete(LoginRequiredMixin, DeleteView):
    model = Artist
    slug_field = 'artist_id'
    template_name = 'artist/artist_delete.html'
    success_url = reverse_lazy('profile')

    # need to check if user is owner of artist before allowing update
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(artist_owner=owner)


class ArtistDirectory(ListView):
    model = Artist
    template_name = 'artist/artist_directory.html'

