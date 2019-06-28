from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete

# Create your models here.


class Venue(models.Model):
    venue_owner = models.OneToOneField(User, on_delete=models.CASCADE)
    venue_id = models.SlugField(max_length=80, default='')
    venue_name = models.CharField(max_length=80)
    venue_description = models.CharField(
        max_length=250, null=True, blank=True)
    

@receiver(pre_delete, sender=Venue, dispatch_uid='question_delete_signal')
def reset_account_type(sender, instance, using, **kwargs):
    user = instance.venue_owner
    user.profile.account_type = 'none'
    user.save()
