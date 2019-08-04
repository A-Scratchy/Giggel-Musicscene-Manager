from django.test import LiveServerTestCase, Client
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from django.contrib.auth.models import User
from venue.models import Venue


class VenueTestsAnonUser(LiveServerTestCase):
    fixtures = ['user_fixtures.json',
                'venue_fixtures.json']

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)

    def test_venue_read_anon(self):
        self.browser.get(self.live_server_url + reverse('venue_detail',
                         args=('111111',)))
        self.assertIn('TestVenue1',
                      self.browser.find_element_by_id('venue_name').text)


class VenueTestsNewUser(LiveServerTestCase):
    fixtures = ['user_fixtures.json']

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)
        # get a user and make sure they are logged in for each test
        self.user = User.objects.get(pk=1)
        client = Client()
        client.force_login(self.user)
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({
                       'name': 'sessionid',
                       'value': client.cookies.get('sessionid').value
                                 })

    def tearDown(self):
        self.browser.quit()

    def test_user_is_logged_in(self):
        self.assertIn('TestUser1', self.user.username)

        # User goes to thier profile and clicks to create a new venue [TO-DO]
        # User fills in form and submits
        # User is taken to the venue dashboard and information is displayed
    def test_create_venue(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('myProfile').click()
        self.browser.find_element_by_id('create_venue').click()
        self.assertIn('Update venue', self.browser.title)
        self.browser.find_element_by_id('id_venue_id').send_keys('99999')
        self.browser.find_element_by_id('id_venue_name').send_keys('testVenue99')
        self.browser.find_element_by_id('submit').click()
        self.assertIn('Venue', self.browser.title)
        self.assertIn('testVenue99', self.browser.find_element_by_id(
            'venue_name').text)

        # No anonymous user can access the edit page
    # def test_anon_user_cannot_modify_an_venue_profile(self):
    #     self.browser.get(self.live_server_url + reverse('venue_dashboard'))
    #     self.assertIn('Login', self.browser.title)


class VenueTestsExistingUser(LiveServerTestCase):
    # populate test DB with predfined instances of models.
    fixtures = [
                'user_fixtures.json',
                'venue_fixtures.json'
               ]

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)
        # get a user and make sure they are logged in for each test
        self.user = User.objects.get(pk=1)
        self.user.profile.account_type = 'venue'
        self.user.save()
        client = Client()
        client.force_login(self.user)
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({
                       'name': 'sessionid',
                       'value': client.cookies.get('sessionid').value
                                 })

    # def test_venue_read_dashboard(self):
    #     self.browser.get(self.live_server_url + reverse('profile'))
    #     self.assertIn('TestUser1', self.browser.find_element_by_id(
    #         'username').text)
    #     self.browser.find_element_by_id('venue_dashboard').click()
    #     self.assertIn('TestVenue1', self.browser.find_element_by_id(
    #         'venue_name').text)

        # User goes to thier profile and loads up thier venue
        # User clicks modify and adds a new description
        # User clicks save and description is now present on the
        # live venue profile

    def test_venue_update(self):
        self.browser.get(self.live_server_url + reverse('profile'))
        self.browser.find_element_by_id('venue_update').click()
        self.assertIn('Update venue', self.browser.title)
        new_description = 'a description of an venue'
        self.browser.find_element_by_id(
            'id_venue_description').send_keys(new_description)
        self.browser.find_element_by_id('submit').click()
        self.assertIn(new_description, self.browser.find_element_by_id(
            'venue_description').text)

    def test_venue_delete(self):
        self.browser.get(self.live_server_url + reverse('profile'))
        self.browser.find_element_by_id('venue_delete').click()
        self.browser.find_element_by_id('submit').click()
        self.browser.get(self.live_server_url
                         + reverse('venue_detail', args=('111111',)))
        self.assertNotIn('Venue', self.browser.title)

    def test_venue_directory(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('venue_directory').click()
        self.assertIn('Venue directory', self.browser.title)
        self.assertIn('TestVenue1',
                      self.browser.find_element_by_id('111111_venue_name').text)
