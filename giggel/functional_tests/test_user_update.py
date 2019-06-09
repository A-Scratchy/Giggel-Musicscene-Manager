from django.test import LiveServerTestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from .helper_methods import helperMethods
import time
# 54


class loggedInFunctionalTests(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(4)
        self.username = 'MrTest'
        self.password = 'RandomPassword#11'
        self.session_cookie = helperMethods.create_cookie(
            username=self.username, password=self.password)

    def setUpCookie(self):
        self.browser.get(self.live_server_url + reverse('blankPage'))
        self.browser.add_cookie(self.session_cookie)
        self.browser.refresh()

    def tearDown(self):
        self.browser.quit()

    def test_user_sent_to_profile_after_logging_in(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("login").click()
        self.browser.find_element_by_id(
            "id_username").send_keys(self.username)
        self.browser.find_element_by_id(
            "id_password").send_keys(self.password)
        self.browser.find_element_by_id("submit").click()
        self.assertIn(self.username, self.browser.title)
        self.assertIn('Profile', self.browser.title)

    def test_site_indicates_user_logged_in(self):
        self.setUpCookie()
        self.browser.get(self.live_server_url)
        self.assertIn(self.username, self.browser.find_element_by_name(
            "loggedInUser").text)

    def test_user_sees_correct_info_on_profile(self):
        self.setUpCookie()
        self.browser.get(self.live_server_url + reverse('profile'))
        self.assertIn(
            self.username, self.browser.find_element_by_id("username").text)
        self.assertIn('testUser@test.com',
                      self.browser.find_element_by_id("email").text)

    #     # John decides he wants to change his profile information,
    #     # He clicks the option to modify profile and changes his
    #     # email address to jsmith@test.com

    def test_user_can_update_profile(self):
        new_county = 'Lincolnshire'
        self.setUpCookie()
        self.browser.get(self.live_server_url + reverse('profile'))
        # check we are on the profile detail page and it has old email in
        self.assertIn('testUser@test.com',
                      self.browser.find_element_by_id("email").text)
        self.browser.find_element_by_id("updateProfile").click()
        # check we are on the update page and enter new county
        county = self.browser.find_element_by_id("id_county")
        county.clear()
        county.send_keys(new_county)
        self.browser.find_element_by_id("submit").click()
        # check we have gone back to the profile detail page and new email is present
        self.assertIn('User Profile', self.browser.title)
        self.assertIn(new_county,
                      self.browser.find_element_by_id("id_county").text)
