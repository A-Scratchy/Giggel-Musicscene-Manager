from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_slug = models.SlugField(max_length=80, default='')
    confrimation_status = models.BooleanField(default=False)
    membershipLevel = models.CharField(max_length=15, default='free')
    county = models.CharField(max_length=40, blank=True)
    birth_date = models.DateField(null=True, blank=True)
