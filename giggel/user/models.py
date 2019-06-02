from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_key = models.SlugField(max_length=80, default='')
    confrimation_status = models.BooleanField(default=False)
    membershipLevel = models.CharField(max_length=15, default='free')
    county = models.CharField(
        max_length=40, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
