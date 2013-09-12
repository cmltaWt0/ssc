# coding=utf-8

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


class SSCTestCase(TestCase):
    def setUp(self):
        """
        Preconditions
        """
        self.user = User.objects.create_user('max', 'test@mail.com', 'test')
        self.client = Client()


class HTTPRequestTest(SSCTestCase):
    """
    Testing simple HTTP request behaviour.
    """
    
    def test_unauthorized_access(self):
        """
        Should redirect to login page if not
        authenticated ssc/ and ssc/xml/.
        """
        response = self.client.get('/ssc/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

        response = self.client.get('/ssc/xml/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_rendering_form(self):
        """
        Should render form.html template /ssc/.
        """
        self.client.login(username='max', password='test')

        response = self.client.get('/ssc/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/form.html')

        response = self.client.get('/ssc/xml/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/form.html')

    #TODO stub make_request
    def test_http_behaviour(self):
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/', {'login_name': 'KHaRKoV-x00 PoN 1/1/01/1:01.1.1', 'type': 'raw'}, follow=True)
        self.assertTrue(('<li>No sessions were found which matched the search criteria.</li>' in response.content))


class AjaxRequestTest(SSCTestCase):
    """
    Testing ajax HTTP request behaviour.
    """
    
    def test_unauthorized_access(self):
        """
        Should redirect to login page if not
        authenticated /ssc/ajax/ and /ssc/ajax/xml/.
        """
        response = self.client.get('/ssc/ajax/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

        response = self.client.get('/ssc/ajax/xml/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/login.html')

    def test_ajax(self):
        """
        Should return 'Not implemented yet.'
        """
        self.client.login(username='max', password='test')

        #TODO stub make_request
        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKoV-x00 PoN 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, 'No sessions were found which matched the search criteria.')
        #TODO stub make_request
        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKoV-x00 PoN 1/1/01/1:01.1.1', 'type': 'raw'}, follow=True)
        self.assertTrue(('<li>No sessions were found which matched the search criteria.</li>' in response.content))

        response = self.client.post('/ssc/ajax/xml/', {'login_name': 'test'}, follow=True)
        self.assertTrue(('<li>No sessions were found which matched the search criteria.</li>' in response.content))


class SSCTest(SSCTestCase):
    """
    Test server-side logic.
    """
    def test_syntax_error_handling(self):
        """
        Should return 'Error: ' + ERROR_MSG
        """
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/ajax/', {'login_name': 'test'}, follow=True)
        self.assertEqual(response.content, 'Error: TEST Syntax error.')

        response = self.client.post('/ssc/ajax/', {'login_name': ''}, follow=True)
        self.assertEqual(response.content, 'Error: Syntax error.')

        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKV-k05 PoN 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, 'Error: KHARKV-K05 PON 1/1/01/1:01.1.1 Syntax error.')

        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKoV-x09 PoN 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, 'Error: KHARKOV-X09 PON 1/1/01/1:01.1.1 Syntax error.')

        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKoV-x09 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, 'Error: KHARKOV-X09 1/1/01/1:01.1.1 Syntax error.')

        response = self.client.post('/ssc/ajax/', {'login_name': 'не латин'}, follow=True)
        self.assertEqual(response.content, 'Error: НЕ ЛАТИН Syntax error.')
