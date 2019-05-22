from django.test import LiveServerTestCase
from selenium import webdriver


class basicFunctionalTests(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

        # test home page is loaded
    def test_site_reachable(self):
        browser = self.browser
        browser.get(self.live_server_url)
        self.assertIn('Giggel', browser.title)
