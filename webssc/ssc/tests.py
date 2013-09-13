# coding=utf-8

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


#TODO make complete tests both for default http handler(without javascript/ajax) and for ajax before override with JS.

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
    def test_logic(self):
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/', {'login_name': 'KHaRKoV-x00 PoN 1/1/01/01:1.1.99', 'type': 'raw'}, follow=True)
        self.assertTrue('<li>No sessions were found which matched the search criteria.</li>' in response.content)

        response = self.client.post('/ssc/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                              'opt1': '1', 'opt2': '1', 'opt3': '01', 'opt4': '01', 'opt5': '1',
                                              'opt6': '1', 'opt7': '99', 'type': 'comp'}, follow=True)
        self.assertTrue('<li>No sessions were found which matched the search criteria.</li>' in response.content)

    def test_syntax_error_handling(self):
        """
        Should return 'Error: ' + ERROR_MSG
        """
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/', {'login_name': 'test', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: TEST Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'login_name': '', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'login_name': 'KHaRKV-k05 PoN 1/1/01/1:01.1.1', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: KHARKV-K05 PON 1/1/01/1:01.1.1 Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'login_name': 'KHaRKoV-x09 PoN 1/1/01/1:01.1.1', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: KHARKOV-X09 PON 1/1/01/1:01.1.1 Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'login_name': 'KHaRKoV-x09 1/1/01/1:01.1.1', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: KHARKOV-X09 1/1/01/1:01.1.1 Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'login_name': 'не латин', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: НЕ ЛАТИН Incorrect input/Syntax error.' in response.content)


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

    def test_logic(self):
        """
        Testing common logic.
        """
        self.client.login(username='max', password='test')

        #TODO stub make_request
        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKoV-x00 PoN 1/1/01/01:1.1.99'}, follow=True)
        self.assertEqual(response.content, 'No sessions were found which matched the search criteria.')
        #TODO stub make_request
        response = self.client.post('/ssc/ajax/xml/', {'login_name': 'KHaRKoV-x00 PoN 1/1/01/01:1.1.99'}, follow=True)
        self.assertEqual(response.content, 'No sessions were found which matched the search criteria.')

    def test_syntax_error_handling(self):
        """
        Should return 'Error: ' + ERROR_MSG
        """
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/ajax/', {'login_name': 'test'}, follow=True)
        self.assertEqual(response.content, 'Error: TEST Incorrect input/Syntax error.')

        response = self.client.post('/ssc/ajax/', {'login_name': ''}, follow=True)
        self.assertEqual(response.content, 'Error: Incorrect input/Syntax error.')

        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKV-k05 PoN 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, 'Error: KHARKV-K05 PON 1/1/01/1:01.1.1 Incorrect input/Syntax error.')

        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKoV-x09 PoN 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, 'Error: KHARKOV-X09 PON 1/1/01/1:01.1.1 Incorrect input/Syntax error.')

        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKoV-x09 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, 'Error: KHARKOV-X09 1/1/01/1:01.1.1 Incorrect input/Syntax error.')

        response = self.client.post('/ssc/ajax/', {'login_name': 'не латин'}, follow=True)
        self.assertEqual(response.content, 'Error: НЕ ЛАТИН Incorrect input/Syntax error.')
