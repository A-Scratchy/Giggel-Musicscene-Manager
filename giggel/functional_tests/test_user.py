from django.test import LiveServerTestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time


class TestAnonUser(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)

    def tearDown(self):
        self.browser.quit()

    def fillInRegForm(self, username, password1, password2):
        url = self.live_server_url
        self.browser.get(url)
        self.browser.find_element_by_name('signup').click()
        self.browser.find_element_by_id(
            "id_username").send_keys(username)
        self.browser.find_element_by_id(
            "id_email").send_keys('MrTest@test.com')
        self.browser.find_element_by_id(
            "id_password1").send_keys(password1)
        self.browser.find_element_by_id(
            "id_password2").send_keys(password2)
        self.browser.find_element_by_id("submit").click()

    def test_user_can_create_account(self):
        self.fillInRegForm('MrTest',
                           'APassword123', 'APassword123')
        self.assertIn('Check your inbox', self.browser.title)

    def test_register_form_returns_with_errors_if_invalid(self):
        self.fillInRegForm('MrTest',
                           'GoodPassword', 'BadPassword')
        self.assertIn('Register', self.browser.title)
        text = self.browser.find_element_by_name("error_text").text
        self.assertIn('The two password fields didn\'t match.', text)


class TestNewUser(LiveServerTestCase):
    fixtures = ['user_fixtures.json']

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)
        self.user = User.objects.get(username='TestUser1')

    def test_user_sent_to_profile_after_logging_in(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("login").click()
        self.browser.find_element_by_id(
            "id_username").send_keys(self.user.username)
        self.browser.find_element_by_id(
                "id_password").send_keys('TestPassword1')
        self.browser.find_element_by_id("submit").click()
        self.assertIn(self.user.username, self.browser.title)
        self.assertIn('Profile', self.browser.title)


class TestLoggedInUser(LiveServerTestCase):
    fixtures = ['user_fixtures.json']

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)
        # get a user and make sure they are logged in for each test
        self.user = User.objects.get(username='TestUser1')
        client = Client()
        client.force_login(self.user)
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(
                {'name': 'sessionid',
                 'value': client.cookies.get('sessionid').value
                 })

    def tearDown(self):
        self.browser.quit()

    def test_site_indicates_user_logged_in(self):
        self.browser.get(self.live_server_url)
        self.assertIn(self.user.username, self.browser.find_element_by_name(
            "loggedInUser").text)

    def test_user_sees_correct_info_on_profile(self):
        self.browser.get(self.live_server_url + reverse('profile'))
        self.assertIn(
            self.user.username, self.browser.find_element_by_id("username").text)
        self.assertIn('testuser1@test.com',
                      self.browser.find_element_by_id("email").text)

    def test_user_can_update_profile(self):
        new_county = 'Lincolnshire'
        self.browser.get(self.live_server_url + reverse('profile'))
        # check we are on the profile detail page and it has old email in
        self.assertIn('testuser1@test.com',
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

    def test_user_profile_update_returns_errors(self):
        New_DOB = 'NotADOB'
        self.browser.get(self.live_server_url + reverse('profile'))
        self.assertIn('testuser1@test.com',
                      self.browser.find_element_by_id("email").text)
        self.browser.find_element_by_id("updateProfile").click()
        dob = self.browser.find_element_by_id("id_birth_date")
        dob.clear()
        dob.send_keys(New_DOB)
        self.browser.find_element_by_id("submit").click()
        self.assertIn('Enter a valid date',
                      self.browser.find_element_by_id("messages").text)
