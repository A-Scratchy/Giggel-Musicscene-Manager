from gig.models import Gig
from artist.models import Artist
from venue.models import Venue
from django.test import LiveServerTestCase, Client
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from django.contrib.auth.models import User


class GigTestsAnonUser(LiveServerTestCase):
    fixtures = ['user_fixtures.json',
                'venue_fixtures.json',
                'artist_fixtures.json',
                'gig_fixtures.json']

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)

    def test_gig_read_anon(self):
        self.browser.get(
                self.live_server_url +
                reverse('gig_detail',
                        args=('222222',))
                )
        self.assertIn('Test Gig',
                      self.browser.find_element_by_id('gig_name').text)

    def test_create_venue(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('myProfile').click()
        self.browser.find_element_by_id('my_gigs').click()
        self.browser.find_element_by_id('create_gig').click()
        self.assertIn('Add gig', self.browser.title)
        select = self.browser.find_element_by_id('venue')
        select.select_by_visable_text('TestVenue1')
        self.browser.find_element_by_id('gig_date').send_keys('25/01/2020')
        self.browser.find_element_by_id('submit').click()
        self.assertIn('Gig', self.browser.title)
        self.assertIn('TestVenue1', self.browser.find_element_by_id(
            'venue').text)
        
        # test update

    def test_update_gig(self):
        self.browser.get(
                self.live_server_url +
                reverse('gig_detail',
                        args=('222222',))
                )
        self.assertIn('a test gig', self.browser.find_element_by_id('gig_description').text)
        self.browser.find_element_by_id('update_gig').click()
        self.assertIn('Update gig', self.bnrowser.title)
        self.browser.find_element_by_id('gig_description').send_keys('a new description')
        self.browser.find_element_by_id('submit').click()
        self.assertIn('new description', self.browser.find_element_by_id('gig_description').text)

        # test delete

    def test_delete_gig(self):
        self.browser.get(
                self.live_server_url +
                reverse('gig_detail',
                        args=('222222',))
                )
        self.browser.find_element_by_id('delete_gig').click()
        self.browser.find_element_by_id('submit').click()
        self.assertIn('My gigs', self.browser.title)
        self.browser.get(
                self.live_server_url +
                reverse('gig_detail',
                        args=('222222',))
                )
        self.assertIn('404', self.browser.title)
