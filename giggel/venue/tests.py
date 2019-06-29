from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from .models import Venue
# Unit tests for user app


class BasicUnitTestsVenue(TestCase):

    def test_venue_dashboard_url_retruns_correct_template(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        self.user.venue = Venue.objects.create(venue_owner=self.user,
                                                 venue_name='DJtest',
                                                 venue_id='djtest5364')
        response = self.client.get(reverse('venue_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'venue/venue_dashboard.html')

    def test_venue_detail_url_retruns_correct_template(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        self.user.venue = Venue.objects.create(venue_owner=self.user,
                                                 venue_name='DJtest',
                                                 venue_id='djtest5364')
        url = reverse('venue_detail', args=('djtest5364',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'venue/venue_detail.html')

        # to do
    def test_venue_update_url_returns_correct_template(serlf):
        pass

    def test_venue_dashboard_url_cannot_be_access_anonymously(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.user.venue = Venue.objects.create(venue_owner=self.user,
                                                 venue_name='DJtest',
                                                 venue_id='djtest5364')
        response = self.client.get(reverse('venue_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'venue/venue_dashboard.html')
    
    def test_venue_create_url_creates_and_redirects(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        assert(User.objects.all().filter(venue__isnull=True).exists())
        response = self.client.get(reverse('venue_create'), follow=True)
        self.assertTemplateUsed(
            response, 'venue/venue_update.html')

    def test_venue_directory_url_uses_correct_template(self):
        response = self.client.get(reverse('venue_directory'))
        self.assertTemplateUsed(response, 'venue/venue_directory.html')
