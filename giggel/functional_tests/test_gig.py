from gig.models import Gig
from artist.models import Artist
from venue.models import Venue
from django.test import LiveServerTestCase, Client
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from django.contrib.auth.models import User
import time


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
                'gig_fixtures.json',
                'gig_request_fixtures.json']

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
        e.select_by_visible_text('James pub')
        e = Select(self.browser.find_element_by_id('id_gig_artist'))
        e.select_by_visible_text('Jim')
        e = Select(self.browser.find_element_by_id('id_gig_owner'))
        e.select_by_visible_text('Jim@test.com')
        self.browser.find_element_by_id('id_gig_date').send_keys('01/05/2020')
        self.browser.find_element_by_id('submit').click()
        self.assertIn('My Gigs', self.browser.title)
        self.assertIn('Jim\'s First Gig', self.browser.find_element_by_id(
            'link_Jim\'s First Gig').text)

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


class GigRequestTestsExistingVenueUser(LiveServerTestCase):
    fixtures = ['user_fixtures.json',
                'venue_fixtures.json',
                'artist_fixtures.json',
                'gig_fixtures.json',
                'gig_request_fixtures.json']

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)
        # get a user and make sure they are logged in for each test
        self.user = User.objects.get(username='james@test.com')
        self.user.profile.account_type = 'venue'
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

    def test_artist_request_create(self):
        self.browser.get(self.live_server_url + reverse('artist_detail',
                         args=('f0MPVSK4bsye8rSxzOdZ',)))
        self.browser.find_element_by_id('request_gig_from_artist').click()
        self.assertIn('Request', self.browser.title)
        self.browser.find_element_by_id('id_gig_request_name').send_keys('TestReq3')
        self.browser.find_element_by_id('id_gig_request_description').send_keys('a description')
        self.browser.find_element_by_id('id_gig_request_date').send_keys('01/01/2020')
        self.browser.find_element_by_id('submit').click()
        self.assertIn('created successfully', self.browser.find_element_by_id('messages').text)
        self.assertIn('TestReq3', self.browser.find_element_by_id('link_TestReq3').text)


    def test_artist_request_read(self):
        # addfixture to create request
        self.browser.get(self.live_server_url + reverse('venue_dashboard'))
        self.assertIn('Jim', self.browser.find_element_by_id('link_GigReqTest2').text)
        self.browser.find_element_by_id('link_GigReqTest2').click()
        self.assertIn('Jim', self.browser.find_element_by_id('gig_request_artist').text)

    def test_artist_request_update(self):
        # addfixture to create request
        self.browser.get(self.live_server_url + reverse('venue_dashboard'))
        self.assertIn('GigReqTest2', self.browser.find_element_by_id('link_GigReqTest2').text)
        self.browser.find_element_by_id('link_GigReqTest2').click()
        gig_id = self.browser.find_element_by_id('gig_request_id').text
        self.browser.find_element_by_id('update_gig_request').click()
        self.browser.find_element_by_id('id_gig_request_description').clear()
        self.browser.find_element_by_id('id_gig_request_description').send_keys('a new description')
        self.browser.find_element_by_id('submit').click()
        self.browser.find_element_by_id('venue_dashboard').click()
        self.browser.find_element_by_id('link_GigReqTest2').click()
        self.assertIn('a new description', self.browser.find_element_by_id('gig_request_description').text)

    def test_artist_request_delete(self):
        self.browser.get(self.live_server_url + reverse('venue_dashboard'))
        self.assertIn('GigReqTest2', self.browser.find_element_by_id('link_GigReqTest2').text)
        self.browser.find_element_by_id('link_GigReqTest2').click()
        self.browser.find_element_by_id('delete_request').click()
        self.browser.find_element_by_id('submit').click()
        self.assertIn('deleted', self.browser.find_element_by_id('messages').text)
        #logic to see if object delteted

    def test_artist_request_respond(self):
        # addfixture to create request
        self.browser.get(self.live_server_url + reverse('venue_dashboard'))
        self.assertIn('Jim', self.browser.find_element_by_id('link_GigReqTest2').text)
        self.browser.find_element_by_id('link_GigReqTest2').click()
        self.browser.find_element_by_id('submit').click()
        self.browser.get(self.live_server_url + reverse('my_gigs'))
        self.assertIn('James pub', self.browser.find_element_by_id('link_GigReqTest2').text)

class GigRequestTestsExistingArtistUser(LiveServerTestCase):
    fixtures = ['user_fixtures.json',
                'venue_fixtures.json',
                'artist_fixtures.json',
                'gig_fixtures.json',
                'gig_request_fixtures.json']

    def setUp(self):
        options = Options()
        options.set_headless(headless=True)
        self.browser = webdriver.Firefox(
            firefox_options=options)
        self.browser.implicitly_wait(1)
        # get a user and make sure they are logged in for each test
        self.user = User.objects.get(username='jim@test.com')
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

        #User with an artist goes to a venue detail page
        #User clicks requeast to play at venue
        #A requestgigVenue is created with to, from, time and gig_description
        #request is default unconfirmed
        #request shows up in artists dashboard
        #requset can be confirmed or denied by venue owner

        def test_venue_request_create(self):
            self.browser.get(self.live_server_url + reverse('venue_detail',
                             args=('lT75sSwrUWcVieIYIaQs',)))
            self.browser.find_element_by_id('request_gig_at_venue').click()
            self.assertIn('Request', self.browser.title)
            self.browser.find_element_by_id('id_gig_request_name').send_keys('TestReq5')
            self.browser.find_element_by_id('id_gig_request_description').send_keys('a description')
            self.browser.find_element_by_id('id_gig_request_date').send_keys('01/01/2020')
            self.browser.find_element_by_id('submit').click()
            self.assertIn('created successfully', self.browser.find_element_by_id('messages').text)
            self.assertIn('TestReq5', self.browser.find_element_by_id('link_TestReq5').text)

        def test_venue_request_read(self):
            # addfixture to create request
            self.browser.get(self.live_server_url + reverse('artist_dashboard'))
            self.assertIn('James pub', self.browser.find_element_by_id('link_GigReqTest3').text)
            self.browser.find_element_by_id('link_GigReqTest3').click()
            self.assertIn('James pub', self.browser.find_element_by_id('gig_request_venue').text)

        def test_venue_request_update(self):
            # addfixture to create request
            self.browser.get(self.live_server_url + reverse('artist_dashboard'))
            self.assertIn('GigReqTest3', self.browser.find_element_by_id('link_GigReqTest3').text)
            self.browser.find_element_by_id('link_GigReqTest3').click()
            gig_id = self.browser.find_element_by_id('gig_request_id').text
            self.browser.find_element_by_id('update_gig_request').click()
            self.browser.find_element_by_id('id_gig_request_description').clear()
            self.browser.find_element_by_id('id_gig_request_description').send_keys('a new description')
            self.browser.find_element_by_id('submit').click()
            self.browser.find_element_by_id('link_GigReqTest3').click()
            self.assertIn('a new description', self.browser.find_element_by_id('gig_request_description').text)

        def test_venue_request_delete(self):
            self.browser.get(self.live_server_url + reverse('artist_dashboard'))
            self.assertIn('Jim', self.browser.find_element_by_id('artist_name').text)
            self.assertIn('James pub', self.browser.find_element_by_id('link_GigReqTest3').text)
            self.browser.find_element_by_id('link_GigReqTest3').click()
            self.browser.find_element_by_id('delete_request').click()
            self.browser.find_element_by_id('submit').click()
            self.assertIn('deleted', self.browser.find_element_by_id('messages').text)
            #logic to see if object delteted

        def test_venue_request_respond(self):
            # addfixture to create request
            self.browser.get(self.live_server_url + reverse('artist_dashboard'))
            self.assertIn('James pub', self.browser.find_element_by_id('link_GigReqTest3').text)
            self.browser.find_element_by_id('link_GigReqTest3').click()
            self.browser.find_element_by_id('submit').click()
            self.browser.get(self.live_server_url + reverse('my_gigs'))
            self.assertIn('James pub', self.browser.find_element_by_id('link_GigReqTest3').text)
