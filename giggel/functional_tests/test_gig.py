from gig.models import Gig
from artist.models import Artist
from venue.models import Venue
from django.test import LiveServerTestCase, Client
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
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

    def tearDown(self):
        self.browser.quit()

    def test_gig_read_anon(self):
        self.browser.get(
                self.live_server_url +
                reverse('gig_detail',
                        args=('123kjgh123KVh1',))
                )
        self.assertIn('Jim\'s First Gig',
                      self.browser.find_element_by_id('gig_name').text)


class GigTestsExistingUser(LiveServerTestCase):
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
        # get a user and make sure they are logged in for each test
        self.user = User.objects.get(username='Jim@test.com')
        self.user.profile.account_type = 'artist'
        self.user.save()
        client = Client()
        client.force_login(self.user)
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({
                       'name': 'sessionid',
                       'value': client.cookies.get('sessionid').value
                                 })

    def tearDown(self):
        self.browser.quit()

    def test_create_gig(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('myProfile').click()
        self.browser.find_element_by_id('my_gigs').click()
        self.browser.find_element_by_id('create_gig').click()
        self.assertIn('Create gig', self.browser.title)
        self.browser.find_element_by_id('id_gig_id').send_keys('234kjg2h34')
        self.browser.find_element_by_id('id_gig_name').send_keys('TestGig')
        e = Select(self.browser.find_element_by_id('id_gig_venue'))
        e.select_by_visible_text('Jame\'s pub')
        e = Select(self.browser.find_element_by_id('id_gig_artist'))
        e.select_by_visible_text('Jim')
        e = Select(self.browser.find_element_by_id('id_gig_owner'))
        e.select_by_visible_text('Jim@test.com')
        self.browser.find_element_by_id('id_gig_date').send_keys('01/05/2020')
        self.browser.find_element_by_id('submit').click()
        self.assertIn('My Gigs', self.browser.title)
        self.assertIn('Jim\'s First Gig', self.browser.find_element_by_id(
            'Jim\'s First Gig').text)
        
        # test update

    def test_update_gig(self):
        self.browser.get(
                self.live_server_url +
                reverse('gig_detail',
                        args=('123kjgh123KVh1',))
                )
        self.assertIn('Jim\'s first ever gig!', self.browser.find_element_by_id('gig_description').text)
        self.browser.find_element_by_id('update_gig').click()
        self.assertIn('Update gig', self.browser.title)
        self.browser.find_element_by_id('id_gig_description').send_keys('a new description')
        self.browser.find_element_by_id('submit').click()
        self.browser.get(
                self.live_server_url +
                reverse('gig_detail',
                        args=('123kjgh123KVh1',))
                )
        self.assertIn('a new description', self.browser.find_element_by_id('gig_description').text)

        # test delete
    def test_delete_gig(self):
        self.browser.get(
                self.live_server_url +
                reverse('gig_detail',
                        args=('123kjgh123KVh1',))
                )
        self.assertIn('Jim', self.browser.title)
        self.browser.find_element_by_id('delete_gig').click()
        self.assertIn('DELETE', self.browser.title)
        self.browser.find_element_by_id('submit').click()
        self.browser.get(
                self.live_server_url +
                reverse('gig_detail',
                        args=('123kjgh123KVh1',))
                )
        self.assertNotIn('Jim', self.browser.title)
