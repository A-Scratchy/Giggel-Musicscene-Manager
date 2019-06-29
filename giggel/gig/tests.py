from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from artist.models import Artist
from django.conf import settings
from .models import Gig
# Unit tests for user app


class BasicUnitTestsGig(TestCase):

    def test_gig_detail_url_retruns_correct_template(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        Artist.objects.create(
                artist_owner=self.user,
                artist_id='111111',
                artist_name='TestArtist1'
                )
        Gig.objects.create(
                gig_id='444444',
                gig_owner=self.user,
                gig_artist=self.user.artist,
                gig_venue='222222',
                gig_name='DJtest',
                )
        url = reverse('gig_detail', args=('444444',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'gig/gig_detail.html')

    def test_gig_create_url_returns_correct_template(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        Artist.objects.create(
                artist_owner=self.user,
                artist_id='111111',
                artist_name='TestArtist1'
                )
        url = reverse('gig_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gig/gig_create.html')

    def test_gig_directory_url_uses_correct_template(self):
        response = self.client.get(reverse('gig_directory'))
        self.assertTemplateUsed(response, 'gig/gig_directory.html')

    def test_my_gigs_url_uses_correct_template(self):
        response = self.client.get(reverse('my_gigs'))
        self.assertTemplateUsed(response, 'gig/my_gigs.html')
