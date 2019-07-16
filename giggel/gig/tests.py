from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from artist.models import Artist
from django.conf import settings
from .models import Gig, GigRequest
from venue.models import Venue
# Unit tests for user app


class BasicUnitTestsGig(TestCase):

    def test_gig_detail_url_retruns_correct_template(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        artist = Artist.objects.create(
                    artist_owner=self.user,
                    artist_id='111111',
                    artist_name='TestArtist1'
                )
        venue = Venue.objects.create(
                    venue_owner=User.objects.create_user(username='bob', password='bob'),
                    venue_id='222222',
                    venue_name='testVen3'
                )
        Gig.objects.create(
                gig_id='444444',
                gig_owner=self.user,
                gig_artist=artist,
                gig_venue=venue,
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
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        response = self.client.get(reverse('my_gigs'))
        self.assertTemplateUsed(response, 'gig/my_gigs.html')

    #test_gig_delte_url_returns_correct_template

class BasicUnitTestsGigRequestArtist(TestCase):

    def test_gig_request_detail_url_retruns_correct_template(self):
        #refactor with fixtures
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        artist = Artist.objects.create(
                    artist_owner=self.user,
                    artist_id='111111',
                    artist_name='TestArtist1'
                )
        venue = Venue.objects.create(
                    venue_owner=User.objects.create_user(username='bob', password='bob'),
                    venue_id='222222',
                    venue_name='testVen3'
                )
        gig_request = GigRequest.objects.create(
                gig_request_id='999999',
                gig_request_owner=self.user,
                gig_request_artist=artist,
                gig_request_venue=venue,
                gig_request_description='a description',
                gig_request_date='2020-01-01'
                )
        response = self.client.get(reverse('gig_request_detail', args=('999999',)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'gig/gig_request_detail.html')

    def test_gig_create_url_returns_correct_template(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        artist = Artist.objects.create(
                    artist_owner=self.user,
                    artist_id='111111',
                    artist_name='TestArtist1'
                )
        venue = Venue.objects.create(
                    venue_owner=User.objects.create_user(username='bob', password='bob'),
                    venue_id='222222',
                    venue_name='testVen3'
                )
        url = reverse('gig_request_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gig/gig_request_create.html')

    def test_my_gig_requests_url_uses_correct_template(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        response = self.client.get(reverse('my_gig_requests'))
        self.assertTemplateUsed(response, 'gig/my_gig_requests.html')

    def test_gig_request_delete_url_returns_correct_template(self):
        #refactor with fixtures
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        artist = Artist.objects.create(
                    artist_owner=self.user,
                    artist_id='111111',
                    artist_name='TestArtist1'
                )
        venue = Venue.objects.create(
                    venue_owner=User.objects.create_user(username='bob', password='bob'),
                    venue_id='222222',
                    venue_name='testVen3'
                )
        gig_request = GigRequest.objects.create(
                gig_request_id='999999',
                gig_request_owner=self.user,
                gig_request_artist=artist,
                gig_request_venue=venue,
                gig_request_description='a description',
                gig_request_date='2020-01-01'
                )
        url = reverse('gig_request_delete', args=('999999',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gig/gig_request_delete.html')
