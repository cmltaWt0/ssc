from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


class SSCTestCase(TestCase):
    def setUp(self):
        """Preconditions"""
        self.user = User.objects.create_user('test', 'test@mail.com', 'test')
        self.client = Client()


class HTTPRequestTest(SSCTestCase):
    """Testing simple HTTP request behaviour.
    """
    def test_unauthorized_access(self):
        """Should redirect to login page if not authentificated /ssc/.
        """
        response = self.client.get('/ssc/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_unauthorized_access_xml(self):
        """Should redirect to login page if not authentificated /ssc/xml/.
        """
        response = self.client.get('/ssc/xml/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_rendering_form(self):
        """Should render form.html template /ssc/.
        """
        self.client.login(username='test', password='test')
        response = self.client.get('/ssc/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/form.html')

    def test_rendering_form_xml(self):
        """Should render form.html template /ssc/xml/.
        """
        self.client.login(username='test', password='test')
        response = self.client.get('/ssc/xml/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/form.html')


class AjaxRequestTest(SSCTestCase):
    """Testing ajax HTTP request behaviour.
    """
    def test_unauthorized_access(self):
        """Should redirect to login page if not authentificated /ssc/ajax/.
        """
        response = self.client.get('/ssc/ajax/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_unauthorized_access_xml(self):
        """Should redirect to login page if not authentificated /ssc/ajax/xml/.
        """
        response = self.client.get('/ssc/ajax/xml/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_ajax(self):
        """Should return 'Not implemented yet.'
        """
        self.client.login(username='test', password='test')
        response = self.client.get('/ssc/ajax/', follow=True)
        self.assertEqual(response.content, 'Not implemented yet.')

    def test_ajax_xml(self):
        """Should return 'Not implemented yet.'.
        """
        self.client.login(username='test', password='test')
        response = self.client.get('/ssc/ajax/xml/', follow=True)
        self.assertEqual(response.content, 'Not implemented yet.')
