from django.test import LiveServerTestCase
from django.contrib.auth.models import User
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
        welcome = browser.find_element_by_id("messages").text
        self.assertIn(username, welcome)

    def test_site_indicates_user_logged_in(self):
        username = self.generate_string(9)
        password = self.generate_string(9)
        self.user = User.objects.create_user(
            username=username, password=password)
        browser = self.browser
        url = self.live_server_url
        browser.get(url)
        browser.find_element_by_name("login").click()
        browser.find_element_by_id("id_username").send_keys(username)
        browser.find_element_by_id("id_password").send_keys(password)
        browser.find_element_by_id("submit").click()
        loggedInUser = browser.find_element_by_name("loggedInUser").text
        self.assertIn(username, loggedInUser)
