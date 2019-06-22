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
    context_object_name = 'artist'


class ArtistDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'artist/artist_dashboard.html'
    login_url = reverse_lazy('login')


class ArtistCreate(LoginRequiredMixin, CreateView):
    model = Artist
    fields = ['artist_id', 'artist_owner', 'artist_name', 'artist_description']
    template_name = 'artist/artist_create.html'
    success_url = reverse_lazy('profile')
    # form_class = ContactForm


class ArtistUpdate(LoginRequiredMixin, UpdateView):
    #need to check if user is owner of artist before allowing update
    model = Artist
    fields = ['artist_id', 'artist_owner', 'artist_name', 'artist_description']
    template_name = 'artist/artist_update.html'
    slug_field = 'artist_id'
    success_url = reverse_lazy('artist_dashboard')


class ArtistDelte(LoginRequiredMixin, DeleteView):
    model = Artist
    slug_field = 'artist_id'
    template_name = 'artist/artist_delete.html'
    success_url = reverse_lazy('profile')

    #need to check if user is owner of artist before allowing update
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(artist_owner=owner)

def artist_create_auto(request):
    user = request.user
    try:
        user.artist
    except Artist.DoesNotExist:
        return redirect(reverse_lazy('profile'))
    else:
        Artist.objects.create(artist_owner=user, artist_name='')


    
