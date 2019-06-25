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
        self.user.artist = Artist.objects.create(artist_owner=self.user,
                                                 artist_name='DJtest',
                                                 artist_id='djtest5364')
        response = self.client.get(reverse('artist_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'artist/artist_dashboard.html')

    def test_artist_detail_url_retruns_correct_template(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        self.user.artist = Artist.objects.create(artist_owner=self.user,
                                                 artist_name='DJtest',
                                                 artist_id='djtest5364')
        url = reverse('artist_detail', args=('djtest5364',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'artist/artist_detail.html')

    def test_artist_dashboard_url_cannot_be_access_anonymously(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.user.artist = Artist.objects.create(artist_owner=self.user,
                                                 artist_name='DJtest',
                                                 artist_id='djtest5364')
        response = self.client.get(reverse('artist_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'artist/artist_dashboard.html')
    
    def test_artist_create_url_creates_and_redirects(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        assert(User.objects.all().filter(artist__isnull=True).exists())
        response = self.client.get(reverse('artist_create'), follow=True)
        self.assertTemplateUsed(
            response, 'artist/artist_update.html')

    def test_artist_directory_url_uses_correct_template(self):
        response = self.client.get(reverse('artist_directory'))
        self.assertTemplateUsed(response, 'artist/artist_directory')
