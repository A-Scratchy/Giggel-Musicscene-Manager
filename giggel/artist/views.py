from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, TemplateView, View, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from .models import Artist
from gig.models import Gig, GigRequest
import random
import string
# Create your views here.


class ArtistDetail(DetailView):
    model = Artist
    template_name = 'artist/artist_detail.html'
    slug_field = 'artist_id'
    context_object_name = 'artist'


class ArtistDashboard(LoginRequiredMixin, ListView):
    model = Artist
    template_name = 'artist/artist_dashboard.html'
    login_url = reverse_lazy('login')

    # def get_queryset(self):
    #     owner = self.request.user
    #     return GigRequest.objects.filter(gig_request_artist=self.request.user.artist)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        owner = self.request.user
        context['gig_requests'] = GigRequest.objects.filter(gig_request_artist=self.request.user.artist)
        context['gigs'] = Gig.objects.filter(gig_artist=self.request.user.artist)
        return context



class ArtistCreate(View):
    def get(self, request):
        user = request.user
        try:
            user.artist
            messages.add_message(self.request, messages.WARNING, 'you already have an artist')
        except Artist.DoesNotExist:

            artist_id = "".join(
                    [random.choice(string.digits +
                                   string.ascii_letters) for i in range(20)]
                    )

            user.artist = Artist.objects.create(artist_owner=user, artist_name="", artist_id=artist_id)
            user.profile.account_type = 'artist'
            user.save()
            return HttpResponseRedirect(reverse_lazy('artist_update', kwargs={'slug':artist_id}))
        else:
            return HttpResponseRedirect(reverse_lazy('artist_dashboard'))


class ArtistUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    # need to check if user is owner of artist before allowing update
    model = Artist
    slug_field = 'artist_id'
    fields = ['artist_id', 'artist_owner', 'artist_name', 'artist_description']
    template_name = 'artist/artist_update.html'
    success_url = reverse_lazy('artist_dashboard')
    success_message = '%(artist_name)s has been updated successfully'


class ArtistDelete(LoginRequiredMixin, DeleteView):
    model = Artist
    slug_field = 'artist_id'
    template_name = 'artist/artist_delete.html'
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        messages.warning(request, 'Artist has been deleted')
        return super().post(self, request, *args, **kwargs)

    # need to check if user is owner of artist before allowing update
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(artist_owner=owner)


class ArtistDirectory(ListView):
    model = Artist
    template_name = 'artist/artist_directory.html'
