from django.db import models
from django.contrib.auth.models import User
from artist.models import Artist
from venue.models import Venue

# Create your models here.


class Gig(models.Model):
    gig_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    gig_id = models.SlugField(max_length=80, default='')
    gig_artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=True, null=True)
    gig_venue = models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True, null=True)
    gig_name = models.CharField(max_length=80)
    gig_date = models.DateField(null=True, blank=True)
    gig_description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.gig_name
