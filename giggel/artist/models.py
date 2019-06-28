from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete

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


@receiver(pre_delete, sender=Artist, dispatch_uid='question_delete_signal')
def reset_account_type(sender, instance, using, **kwargs):
    user = instance.artist_owner
    user.profile.account_type = 'none'
    user.save()
