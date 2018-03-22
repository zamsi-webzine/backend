from django.urls import reverse, resolve
from rest_framework.test import APILiveServerTestCase

from .apis import Signup


class UserSignUpTest(APILiveServerTestCase):
    def setUp(self):
        self.URL_API_SIGNUP_NAME = 'authentication:signup'
        self.URL_API_SIGNUP = '/auth/signup/'
        self.SIGNUP_VIEW_CLASS = Signup

    def test_signup_url_name_reverse(self):
        url = reverse(self.URL_API_SIGNUP_NAME)
        self.assertEqual(url, self.URL_API_SIGNUP)

    def test_signup_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_API_SIGNUP)
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_SIGNUP_NAME)
        self.assertEqual(
            resolver_match.func.view_class,
            self.SIGNUP_VIEW_CLASS
        )

