from django.test import LiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from selenium import webdriver
import string
import random


class helperMethods():

        # helper method - random string generator
    def generate_string(length):
        randString = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=length))
        return randString


class basicFunctionalTests(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def test_home_page_is_loaded(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Giggel', self.browser.title)

    def test_login_button_present(self):
        self.browser.get(self.live_server_url)
        self.assertTrue(self.browser.find_element_by_name("login"))

    def test_user_can_create_account(self):
        url = self.live_server_url + reverse('register')
        new_username = helperMethods.generate_string(9)
        new_password = helperMethods.generate_string(9)
        self.browser.get(url)
        self.browser.find_element_by_id("id_username").send_keys(new_username)
        self.browser.find_element_by_id(
            "id_password1").send_keys(new_password)
        self.browser.find_element_by_id(
            "id_password2").send_keys(new_password)
        self.browser.find_element_by_id("submit").click()
        welcome = self.browser.find_element_by_id("messages").text
        self.assertIn(new_username, welcome)


class loggedInFunctionalTests(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)
        # create a user to log in with
        self.username = helperMethods.generate_string(9)
        self.password = helperMethods.generate_string(9)
        self.user = User.objects.create_user(
            username=self.username, password=self.password)

    def tearDown(self):
        self.browser.quit()

    def test_site_indicates_user_logged_in(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("login").click()
        self.browser.find_element_by_id("id_username").send_keys(self.username)
        self.browser.find_element_by_id("id_password").send_keys(self.password)
        self.browser.find_element_by_id("submit").click()
        self.assertIn(self.username, self.browser.find_element_by_name(
            "loggedInUser").text)
