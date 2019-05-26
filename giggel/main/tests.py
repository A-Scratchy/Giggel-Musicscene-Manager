from django.test import TestCase

# unit tests for main app


class BasicUnitTestsMain(TestCase):

    def test_url_retruns_correct_template_for_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')
