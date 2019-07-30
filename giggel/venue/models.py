from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete

# Create your models here.


class Venue(models.Model):
    venue_owner = models.OneToOneField(User, on_delete=models.CASCADE)
    venue_id = models.SlugField(max_length=80, default='')
    venue_name = models.CharField(max_length=80)
    venue_town = models.CharField(max_length=100, null=True, blank=True)
    venue_description = models.CharField(
        max_length=250, null=True, blank=True)
    venue_profile_pic = models.ImageField(upload_to="img/venue_profile", null=True, blank=True)
    venue_genres = models.CharField(max_length=200, null=True, blank=True)
    venue_location = models.CharField(max_length=100)

    def __str__(self):
        return self.venue_name

@receiver(pre_delete, sender=Venue, dispatch_uid='question_delete_signal')
def reset_account_type(sender, instance, using, **kwargs):
    user = instance.venue_owner
    user.profile.account_type = 'none'
    user.save()
