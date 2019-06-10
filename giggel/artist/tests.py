from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from .models import Artist
# Unit tests for user app


class BasicUnitTestsArtist(TestCase):

    def test_artist_dashboard_url_retruns_correct_template(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        self.user.artist = Artist.objects.create(
            name='DJtest', artist_id='#djtest5364')
        response = self.client.get(reverse('artist_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'artist/artist_dashboard.html')

    def test_artist_profile_url_retruns_correct_template(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        self.user.artist = Artist.objects.create(name='DJtest')
        artist_id = '#djtest5364'
        response = self.client.get(reverse('artist_profile') + artist_id)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'artist/artist_dashboard.html')

    def test_artist_dashboard_url_cannot_be_access_anonymously(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.user.artist = Artist.objects.create(
            name='DJtest', artist_id='#djtest5364')
        response = self.client.get(reverse('artist_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(
            response, 'artist/login.html')
