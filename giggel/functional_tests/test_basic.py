from django.test import LiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from .helper_methods import helperMethods


class basicFunctionalTests(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)
        self.new_username = helperMethods.generate_string(9)
        self.new_password = helperMethods.generate_string(9)

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

    def test_home_page_is_loaded(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Giggel', self.browser.title)

    def test_login_button_present(self):
        self.browser.get(self.live_server_url)
        self.assertTrue(self.browser.find_element_by_name("login"))

    def test_user_can_create_account(self):
        self.fillInRegForm(self.new_username,
                           self.new_password, self.new_password)
        self.assertIn('Check your inbox', self.browser.title)

    def test_register_form_returns_with_errors_if_invalid(self):
        self.fillInRegForm(self.new_username,
                           self.new_password, 'BadPassword')
        self.assertIn('Register', self.browser.title)
        text = self.browser.find_element_by_name("error_text").text
        self.assertIn('The two password fields didn\'t match.', text)
