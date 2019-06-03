from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
import string
import random


class helperMethods():

        # helper method - random string generator
    def generate_string(length):
        randString = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=length))
        return randString

        # creates a session cookie
    def create_cookie(username, password):
        user = User.objects.create_user(username=username, password=password, first_name='Mr', last_name='test',
                                        email='testUser@test.com')
        user.profile.county = 'Yorkshire'
        user.profile.birth_date = '1999-01-01'
        user.save()
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()
        cookie = {
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'secure': False,
            'path': '/',
        }
        return cookie
