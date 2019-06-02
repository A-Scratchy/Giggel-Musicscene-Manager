from django.test import LiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from selenium import webdriver
from .helper_methods import helperMethods


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
        self.browser.find_element_by_id(
            "id_county").send_keys('Yorkshire')
        self.browser.find_element_by_id(
            "id_birth_date").send_keys('1991-06-02')
        self.browser.find_element_by_id("submit").click()
        welcome = self.browser.find_element_by_id("messages").text
        self.assertIn(new_username, welcome)
        self.assertIn(new_username, self.browser.title)
        self.assertIn('Profile', self.browser.title)

    def test_register_form_returns_with_errors_if_invalid(self):
        url = self.live_server_url + reverse('register')
        new_username = helperMethods.generate_string(9)
        self.browser.get(url)
        self.browser.find_element_by_id("id_username").send_keys(new_username)
        self.browser.find_element_by_id(
            "id_password1").send_keys('test1')
        self.browser.find_element_by_id(
            "id_password2").send_keys('test2')
        self.browser.find_element_by_id(
            "id_county").send_keys('Yorkshire')
        self.browser.find_element_by_id(
            "id_birth_date").send_keys('1991-06-02')
        self.browser.find_element_by_id("submit").click()
        self.assertIn('Register', self.browser.title)
        messages = self.browser.find_element_by_id("messages").text
        self.assertIn('contains errors', messages)

    def test_cannot_access_profile_when_not_logged_in(self):
        url = self.live_server_url + reverse('profile')
        self.assertNotIn('Profile', self.browser.title)
