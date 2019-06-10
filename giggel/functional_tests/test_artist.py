from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from .helper_methods import helperMethods


class basicFunctionalArtistTests(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)
        self.username = 'MrTest'
        self.password = 'RandomPassword#11'
        self.session_cookie = helperMethods.create_cookie(
            username=self.username, password=self.password)

    def tearDown(self):
        self.browser.quit()

    def setUpCookie(self):
        self.browser.get(self.live_server_url + reverse('blankPage'))
        self.browser.add_cookie(self.session_cookie)
        self.browser.refresh()

        # User goes to thier profile and loads up thier artist
        # Artist dashboard is presented with options to edit profile.
    def test_user_can_reach_thier_artist_profile(self):
        self.setUpCookie()
        self.browser.get(self.live_server_url + reverse('profile'))
        self.browser.find_element_by_id('artist_dashboard').click()
        self.assertIn('Artist', self.browser.title)
        # more specific info relating to artist in fixture

        # User goes to thier profile and loads up thier artist
        # User clicks save and description is now present on the live artist profile
    def test_user_can_modify_thier_artist_profile(self):
        self.setUpCookie()
        self.browser.get(self.live_server_url + reverse('profile'))
        self.browser.find_element_by_id('artist_dashboard').click()
        self.assertIn('Artist', self.browser.title)
        new_description = 'a description of an artist'
        self.find_element_by_id(
            'Artist_description').send_keys(new_description)
        artist_id = 'some_artist_id'
        self.browser.get(self.live_server_url + reverse('profile') + artist_id)
        self.assertIn(new_description, self.find_element_by_id(
            'Artist_description'))

        # No anonymous user can access the edit page
    def test_anon_user_cannot_modify_an_artist_profile(self):
        self.setUpCookie()
        self.browser.get(self.live_server_url + reverse('artist_dashboard'))
        self.asserNotIn('Artist', self.browser.title)
