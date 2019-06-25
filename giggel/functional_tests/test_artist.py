from django.test import LiveServerTestCase, Client
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from django.contrib.auth.models import User
from artist.models import Artist
from django.core.management import call_command
import time


class ArtistTestsAnonUser(LiveServerTestCase):
    fixtures = ['user_fixtures.json','profile_fixtures.json','artist_fixtures.json']

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)

    def test_artist_read_anon(self):
        self.browser.get(self.live_server_url + reverse('artist_detail',
            args=('111111',)))
        self.assertIn('artist name: TestArtist1',
                self.browser.find_element_by_id('artist_name').text)


class ArtistTestsNewUser(LiveServerTestCase):
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
        self.browser.add_cookie({'name':'sessionid',
            'value':client.cookies.get('sessionid').value})

    def tearDown(self):
        self.browser.quit()

    def test_user_is_logged_in(self):
        self.assertIn('TestUser1', self.user.username)

        # User goes to thier profile and clicks to create a new artist [TO-DO]
        # User fills in form and submits
        # User is taken to the artist dashboard and information is displayed
    def test_create_artist(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('myProfile').click()
        self.browser.find_element_by_id('create_artven').click()
        self.assertIn('Choose', self.browser.title)
        self.browser.find_element_by_id('create_artist').click()
        self.assertIn('Update artist', self.browser.title)
        self.browser.find_element_by_id('id_artist_id').send_keys('99999')
        self.browser.find_element_by_id('id_artist_name').send_keys('testArtist99')
        self.browser.find_element_by_id('submit').click()
        self.assertIn('Artist', self.browser.title)
        self.assertIn('testArtist99', self.browser.find_element_by_id(
            'artist_name').text)

        # No anonymous user can access the edit page
    # def test_anon_user_cannot_modify_an_artist_profile(self):
    #     self.browser.get(self.live_server_url + reverse('artist_dashboard'))
    #     self.assertIn('Login', self.browser.title)


class ArtistTestsExistingUser(LiveServerTestCase):
    fixtures = ['user_fixtures.json', 'artist_fixtures.json']

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)
        # get a user and make sure they are logged in for each test
        self.user =  User.objects.get(pk=1)
        client = Client()
        client.force_login(self.user)
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({'name':'sessionid',
            'value':client.cookies.get('sessionid').value})

    def test_artist_read_dashboard(self):
        self.browser.get(self.live_server_url + reverse('profile'))
        self.assertIn('TestUser1', self.browser.find_element_by_id(
            'username').text)
        self.browser.find_element_by_id('artist_dashboard').click()
        self.assertIn('TestArtist1', self.browser.find_element_by_id(
            'artist_name').text)

        # User goes to thier profile and loads up thier artist
        # User clicks modify and adds a new description
        # User clicks save and description is now present on the 
        # live artist profile
    def test_artist_update(self):
        self.browser.get(self.live_server_url + reverse('profile'))
        self.assertIn('Profile', self.browser.title)
        self.browser.find_element_by_id('artist_dashboard').click()
        self.browser.find_element_by_id('artist_update').click()
        self.assertIn('Update artist', self.browser.title)
        new_description = 'a description of an artist'
        self.browser.find_element_by_id(
            'id_artist_description').send_keys(new_description)
        self.browser.find_element_by_id('submit').click()
        self.assertIn(new_description, self.browser.find_element_by_id(
            'artist_description').text)

    def test_artist_delete(self):
        self.browser.get(self.live_server_url + reverse('profile'))
        self.assertIn('Profile', self.browser.title)
        self.browser.find_element_by_id('artist_dashboard').click()
        self.browser.find_element_by_id('artist_delete').click()
        self.browser.find_element_by_id('submit').click()
        self.assertIn('Profile', self.browser.title)
        self.browser.get(self.live_server_url
            + reverse('artist_detail', args=('111111',)))
        self.assertNotIn('Artist', self.browser.title)

    def test_artist_directory(self):
        self.brower.get(self.live_server_url)
        self.browser.find_element_by_id('directories').click()
        self.browser.find_element_by_id('artist_directory').click()
        self.browser.assertIn('Artist directory', self.browser.title)
        self.assertIn('TestArtist1', self.browser.find_element_by_id('artist_name'))
