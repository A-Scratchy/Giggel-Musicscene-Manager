from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, TemplateView, View, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from .models import Venue
from gig.models import Gig, GigRequest
import random
import string
# Create your views here.


class VenueDetail(DetailView):
    model = Venue
    template_name = 'venue/venue_detail.html'
    slug_field = 'venue_id'
    context_object_name = 'venue'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        owner = self.object
        context['gigs'] = Gig.objects.filter(gig_venue=owner)
        return context

# class VenueDashboard(LoginRequiredMixin, TemplateView):
#     model = Venue
#     template_name = 'venue/venue_dashboard.html'
#     login_url = reverse_lazy('login')
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         owner = self.request.user
#         context['gig_requests'] = GigRequest.objects.filter(gig_request_venue=self.request.user.venue)
#         context['gigs'] = Gig.objects.filter(gig_venue=self.request.user.venue)
#         return context



class VenueCreate(View):
    def get(self, request):
        user = request.user
        try:
            user.venue
            messages.add_message(self.request, messages.WARNING, 'you already have an venue')
        except Venue.DoesNotExist:
            venue_id = "".join(
                    [random.choice(string.digits +
                                   string.ascii_letters) for i in range(20)]
                    )
            user.venue = Venue.objects.create(venue_owner=user, venue_name="", venue_id=venue_id)
            # consider changing this auto slug to a randomised number/string to make it hard to guess
            user.profile.account_type = 'venue'
            user.save()
            return HttpResponseRedirect(reverse_lazy('venue_update', kwargs={'slug': venue_id}))
        else:
            return HttpResponseRedirect(reverse_lazy('venue_dashboard'))

class VenueUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    # need to check if user is owner of venue before allowing update
    model = Venue
    slug_field = 'venue_id'
    fields = ['venue_name', 'venue_description', 'venue_profile_pic', 'venue_genres', 'venue_location']
    template_name = 'venue/venue_update.html'
    success_url = reverse_lazy('profile')
    success_message = '%(venue_name)s has been updated successfully'


class VenueDelete(LoginRequiredMixin, DeleteView):
    model = Venue
    slug_field = 'venue_id'
    template_name = 'venue/venue_delete.html'
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        messages.warning(request, 'Venue has been deleted')
        return super().post(self, request, *args, **kwargs)

    # need to check if user is owner of venue before allowing update
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(venue_owner=owner)


class VenueDirectory(ListView):
    model = Venue
    template_name = 'venue/venue_directory.html'
