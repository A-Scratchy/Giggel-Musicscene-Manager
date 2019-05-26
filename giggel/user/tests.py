from django.test import TestCase

# Unit tests for user app


class BasicUnitTestsUsers(TestCase):

    def test_user_register_url_retruns_correct_template(self):
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'users/register.html')
