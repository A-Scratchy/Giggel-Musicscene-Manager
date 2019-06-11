from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Artist(models.Model):
    artist_owner = models.OneToOneField(User, on_delete=models.CASCADE)
    artist_id = models.SlugField(max_length=80, default='')
    artist_name = models.CharField(max_length=80)
    artist_description = models.CharField(
        max_length=250, null=True, blank=True)
    # artist profile pic
    # artist distance willing to travel
    # artist genres, multi select list
