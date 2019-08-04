from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_init
import random
import string

# Create your models here.


class Artist(models.Model):
    artist_owner = models.OneToOneField(User, on_delete=models.CASCADE)
    artist_id = models.SlugField(max_length=80, default='')
    artist_name = models.CharField(max_length=80)
    artist_description = models.CharField(
        max_length=250, null=True, blank=True)
    artist_profile_pic = models.ImageField(upload_to="img/artist_profile", default="/img/artist_profile/user.jpeg")
    artist_genres = models.CharField(max_length=200, blank=True, null=True)
    artist_location = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.artist_name


@receiver(pre_delete, sender=Artist)
def reset_account_type(sender, instance, using, **kwargs):
    user = instance.artist_owner
    user.profile.account_type = 'none'
    user.save()
