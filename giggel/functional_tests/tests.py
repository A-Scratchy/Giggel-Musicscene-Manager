from django.test import LiveServerTestCase
from selenium import webdriver
import string
import random


class basicFunctionalTests(LiveServerTestCase):

        # helper method - random string generator
    def generate_string(self, length):
        randString = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=length))
        return randString

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

        # test home page is loaded
    def test_site_reachable(self):
        browser = self.browser
        browser.get(self.live_server_url)
        self.assertIn('Giggel', browser.title)

    def test_user_can_create_account(self):
        username = self.generate_string(9)
        password = self.generate_string(9)
        browser = self.browser
        url = self.live_server_url + '/register/'
        # print URL to console for debug
        print(url)
        browser.get(url)
        browser.find_element_by_id("id_username").send_keys(username)
        browser.find_element_by_id("id_password1").send_keys(password)
        browser.find_element_by_id("id_password2").send_keys(password)
        browser.find_element_by_id("submit").click()
        time.sleep(self.SLEEP_TIME)
        welcome = browser.find_element_by_id("welcome").text
        assertIn(username, welcome)
