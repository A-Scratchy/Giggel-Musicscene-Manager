from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from artist.models import Artist
from venue.models import Venue

# Create your models here.


class Gig(models.Model):
    gig_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    gig_id = models.SlugField(max_length=80, default='')
    gig_artist = models.ForeignKey(Artist, on_delete=models.CASCADE, default=None)
    gig_venue = models.ForeignKey(Venue, on_delete=models.CASCADE, default=None)
    gig_date = models.DateField(null=True, blank=True)
    gig_description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.gig_name

class GigForm(ModelForm):

    class Meta:
        model = Gig
        fields = ['gig_date', 'gig_description', 'gig_artist', 'gig_venue' ]
        ordering = ['gig_date']
        widgets = {
                'gig_date': forms.DateInput(format='%d-%m-%Y', attrs={'class':'datePicker dates', 'readonly':'true'}),
                }

class GigRequest(models.Model):
    gig_request_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    gig_request_id = models.SlugField(max_length=80, default='')
    gig_request_artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=True, null=True)
    gig_request_venue = models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True, null=True)
    gig_request_date = models.DateField(null=True, blank=True)
    gig_request_message = models.CharField(max_length=250, null=True, blank=True)
    gig_request_confirmed = models.BooleanField(default=False)

    def confirm(self):
        self.gig_request_confirmed = True
        return True

    def __str__(self):
        return self.gig_request_name

class GigRequestForm(ModelForm):

    class Meta:
        model = GigRequest
        fields = ['gig_request_date', 'gig_request_message']
        ordering = ['gig_date']
        widgets = {
        'gig_request_date': forms.DateInput(format='%d-%m-%Y', attrs={'class':'datePicker dates', 'readonly':'true'}),
        'gig_request_artist': forms.Select(attrs={'class':'Picker venueOnly'}),
        'gig_request_venue': forms.Select( attrs={'class':'artistOnly',}),
        }
