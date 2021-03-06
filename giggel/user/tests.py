from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
# Unit tests for user app


class BasicUnitTestsUsers(TestCase):

    username = 'Mr Test'

    def test_user_register_url_retruns_correct_template(self):
        response = self.client.get(reverse('django_registration_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'django_registration/registration_form.html')

    def test_user_profile_url_retruns_correct_template(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

        # TO-DO test redirects if user already logged in

    def test_displays_correct_logged_in_user(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertIn(username, html)

    def test_displays_user_logged_out(self):
        username = 'testUser'
        self.user = User.objects.create_user(
            username=username, password='AB12345')
        self.client.login(username=username, password='AB12345')
        self.client.logout()
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertNotIn(username, html)

    def test_cannot_access_profile_while_logged_out(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        html = response.content.decode('utf8')
        self.assertNotIn('profile', html)

    def test_cannot_access_modify_profile_while_logged_out(self):
        response = self.client.get(reverse('updateProfile', args=(1,)))
        self.assertEqual(response.status_code, 302)
        html = response.content.decode('utf8')
        self.assertNotIn('profile', html)

    def test_user_update_profile_form_displayed_correctly(self):
        self.user = User.objects.create_user(
            username=self.username, password='AB12345')
        self.client.login(username=self.username, password='AB12345')
        response = self.client.get(reverse('updateProfile', args=(self.user.profile.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/update.html')

    def test_email(self):
        self.user = User.objects.create_user(
            username=self.username, password='AB12345', email='ascratcherd@brake.org.uk')
        subject = 'test'
        message = 'some message'
        from_email = settings.DEFAULT_FROM_EMAIL
        self.user.email_user(subject, message, from_email)
