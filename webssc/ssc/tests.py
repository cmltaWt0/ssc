"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client


class HTTPRequestTest(TestCase):
    def setUp(self):
        """Preconditions"""
        self.client = Client()

    def test_login_form(self):
        """Should redirect to login page if not authentificated.
        """
        response = self.client.get('/ssc/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_rendering_form(self):
        """Should render form.html template
        """
        response = self.client.get('/ssc/')


class AjaxRequestTest(TestCase):
    def setUp(self):
        """Preconditions"""
        self.client = Client()

    def test_login_form(self):
        """Should redirect to login page if not authentificated.
        """
        response = self.client.get('/ssc/ajax/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_rendering_form(self):
        """Should render form.html template.
        """
        response = self.client.get('/ssc/ajax/')


class XMLRequestTest(TestCase):
    def setUp(self):
        """Preconditions"""
        self.client = Client()

    def test_login_form(self):
        """Should redirect to login page if not authentificated.
        """
        response = self.client.get('/ssc/xml/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_rendering_form(self):
        """Should render form.html template
        """
        response = self.client.get('/ssc/xml/')