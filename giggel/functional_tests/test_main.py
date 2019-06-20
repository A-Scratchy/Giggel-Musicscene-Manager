from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

class BasicTests(LiveServerTestCase):


    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)

    def tearDown(self):
        self.browser.quit()

    def test_home_page_is_loaded(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Giggel', self.browser.title)

    def test_login_button_present(self):
        self.browser.get(self.live_server_url)
        self.assertTrue(self.browser.find_element_by_name("login"))
