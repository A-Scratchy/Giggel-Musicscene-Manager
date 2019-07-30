from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from artist.models import Artist
from venue.models import Venue


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, null=True, blank=True)
    user_profile_pic = models.ImageField(upload_to="img/user_profile", null=True, blank=True)


    def __str__(self):
        return self.user

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
#    if (User.account_type == 'artist'):
#        Artist.objects.create(user=instance)
#    if (User.account_type == 'venue'):
#        Venue.objects.create(user=instance)
