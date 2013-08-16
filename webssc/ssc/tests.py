from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


class HTTPRequestTest(TestCase):
    def setUp(self):
        """Preconditions"""
        self.user = User.objects.create_user('test', 'test@mail.com', 'test')
        self.client = Client()

    def test_login_form(self):
        """Should redirect to login page if not authentificated.
        """
        response = self.client.get('/ssc/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_login_form_xml(self):
        response = self.client.get('/ssc/xml/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_rendering_form(self):
        """Should render form.html template.
        """
        self.client.login(username='test', password='test')
        response = self.client.get('/ssc/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/form.html')

    def test_rendering_form_xml(self):
        """Should render form.html template.
        """
        self.client.login(username='test', password='test')
        response = self.client.get('/ssc/xml/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/form.html')


class AjaxRequestTest(TestCase):
    def setUp(self):
        """Preconditions"""
        self.user = User.objects.create_user('test', 'test@mail.com', 'test')
        self.client = Client()

    def test_login_form(self):
        """Should redirect to login page if not authentificated.
        """
        response = self.client.get('/ssc/ajax/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_login_form_xml(self):
        """Should redirect to login page if not authentificated.
        """
        response = self.client.get('/ssc/ajax/xml/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_get_call(self):
        """Should return 'False' at first call with method GET
        because template is not rendering but returning HttpResponse object
        """
        self.client.login(username='test', password='test')
        response = self.client.get('/ssc/ajax/', follow=True)
        self.assertEqual(response.content, 'False')

    def test_get_call_xml(self):
        """Should return 'Not implemented yet.'.
        """
        self.client.login(username='test', password='test')
        response = self.client.get('/ssc/ajax/xml/', follow=True)
        self.assertEqual(response.content, 'Not implemented yet.')
