from django.test import LiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from selenium import webdriver
from .helper_methods import helperMethods
import time


class loggedInFunctionalTests(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)
        # create a user to log in with
        self.username = helperMethods.generate_string(9)
        self.password = helperMethods.generate_string(9)
        self.user = User.objects.create_user(
            username=self.username, password=self.password, email='testUser@test.com')

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

    def test_user_sent_to_profile_after_logging_in(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_id("id_username").send_keys(self.username)
        self.browser.find_element_by_id("id_password").send_keys(self.password)
        self.browser.find_element_by_id("submit").click()
        self.assertIn(self.username, self.browser.title)
        self.assertIn('Profile', self.browser.title)

    def test_user_sees_correct_info_on_profile(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_id("id_username").send_keys(self.username)
        self.browser.find_element_by_id("id_password").send_keys(self.password)
        self.browser.find_element_by_id("submit").click()
        self.browser.get(self.live_server_url + reverse('profile'))
        self.assertIn(
            self.username, self.browser.find_element_by_id("username").text)
        self.assertIn('testUser@test.com',
                      self.browser.find_element_by_id("email").text)

        # John decides he wants to change his profile information,
        # He clicks the option to modify profile and changes his
        # email address to jsmith@test.com

    def test_user_can_update_profile(self):
        new_email = 'jsmith@test.com'
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_id("id_username").send_keys(self.username)
        self.browser.find_element_by_id("id_password").send_keys(self.password)
        self.browser.find_element_by_id("submit").click()
        self.browser.get(self.live_server_url + reverse('profile'))
        # check we are on the profile detail page and it has old email in
        self.assertIn('Profile', self.browser.title)
        self.assertIn('testUser@test.com',
                      self.browser.find_element_by_id("email").text)
        self.browser.find_element_by_id("updateProfile").click()
        # check we are on the update page and enter new email
        self.assertIn('Update Profile', self.browser.title)
        self.browser.find_element_by_id("id_email").send_keys('new_email')
        self.browser.find_element_by_id("submit").click()
        # check we have gone back to the profile detail page and new email is present
        self.assertIn('Profile', self.browser.title)
        self.assertIn('new_email',
                      self.browser.find_element_by_id("email").text)
