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
        self.assertTrue('<input type="radio" name="type" value="raw" id="raw" checked>' in response.content)
        self.assertTrue('<input type="radio" name="type" value="comp">' in response.content)
        self.assertTrue('<select style="width:10em;" name="city" id="city">' in response.content)
        self.assertTrue('<select  style="width:5em;" name="point" id="point">' in response.content)
        self.assertTrue('input type="submit" value="Session info"' in response.content)

        response = self.client.get('/ssc/xml/', follow=True)
        self.assertEqual(response.templates[0].name, 'ssc/form.html')
        self.assertTrue('<input type="radio" name="type" value="raw" id="raw" checked>' in response.content)
        self.assertTrue('<input type="radio" name="type" value="comp">' in response.content)
        self.assertTrue('<select style="width:10em;" name="city" id="city">' in response.content)
        self.assertTrue('<select  style="width:5em;" name="point" id="point">' in response.content)
        self.assertTrue('input type="submit" value="Session info"' in response.content)

    #TODO stub make_request and add test for deleting after
    def test_logic(self):
        """
        Testing common logic
        """
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/', {'login_name': 'KHaRKoV-x00 PoN 1/1/01/01:1.1.99', 'type': 'raw'}, follow=True)
        self.assertTrue('<li>No sessions were found which matched the search criteria.</li>' in response.content)

        response = self.client.post('/ssc/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                              'opt1': '001', 'opt2': '001', 'opt3': '001', 'opt4': '001', 'opt5': '001',
                                              'opt6': '01', 'opt7': '099', 'type': 'comp'}, follow=True)
        self.assertTrue('<li>No sessions were found which matched the search criteria.</li>' in response.content)

        response = self.client.post('/ssc/', {'login_name': 'KHARKOV-K13 PON 1/1/04/04:60.1.2', 'type': 'raw'}, follow=True)
        self.assertTrue('KHARKOV-K13 PON 1/1/04/04:60.1.2' in response.content)
        self.assertTrue('Domain=00:02:9b:30:bf:5d' in response.content)
        self.assertTrue('<input type="hidden" name="login_del" value="KHARKOV-K13 PON 1/1/04/04:60.1.2">' in response.content)
        self.assertTrue('<input type="submit" value="Delete" name="submit">' in response.content)
        self.assertTrue('<input type="submit" value="No" name="submit">' in response.content)

        response = self.client.post('/ssc/', {'city': 'KHARKOV', 'point': 'K13', 'login_name': '',
                                    'opt1': '001', 'opt2': '001', 'opt3': '004', 'opt4': '004', 'opt5': '0060',
                                    'opt6': '001', 'opt7': '002', 'type': 'comp'}, follow=True)
        self.assertTrue('KHARKOV-K13 PON 1/1/04/04:60.1.2' in response.content)
        self.assertTrue('Domain=00:02:9b:30:bf:5d' in response.content)
        self.assertTrue('<input type="hidden" name="login_del" value="KHARKOV-K13 PON 1/1/04/04:60.1.2">' in response.content)
        self.assertTrue('<input type="submit" value="Delete" name="submit">' in response.content)
        self.assertTrue('<input type="submit" value="No" name="submit">' in response.content)

    #TODO stub return value
    def test_logic_xml(self):
        """
        Testing common logic.
        """
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/xml/', {'login_name': 'KHaRKoV-x00 PoN 1/1/01/01:1.1.99', 'type': 'raw'}, follow=True)
        self.assertTrue('<li>No sessions were found which matched the search criteria.</li>' in response.content)

        response = self.client.post('/ssc/xml/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                    'opt1': '001', 'opt2': '001', 'opt3': '001', 'opt4': '001', 'opt5': '001',
                                    'opt6': '01', 'opt7': '099', 'type': 'comp'}, follow=True)
        self.assertTrue('<li>No sessions were found which matched the search criteria.</li>' in response.content)

        response = self.client.post('/ssc/xml/', {'login_name': 'KHARKOV-K13 PON 1/1/04/04:60.1.2', 'type': 'raw'}, follow=True)
        self.assertTrue('KHARKOV-K13 PON 1/1/04/04:60.1.2' in response.content)
        self.assertTrue('Domain=00:02:9b:30:bf:5d' in response.content)
        self.assertTrue('<input type="hidden" name="login_del" value="KHARKOV-K13 PON 1/1/04/04:60.1.2">' in response.content)
        self.assertTrue('<input type="submit" value="Delete" name="submit">' in response.content)
        self.assertTrue('<input type="submit" value="No" name="submit">' in response.content)

        response = self.client.post('/ssc/xml/', {'city': 'KHARKOV', 'point': 'K13', 'login_name': '',
                                    'opt1': '001', 'opt2': '001', 'opt3': '004', 'opt4': '004', 'opt5': '0060',
                                    'opt6': '001', 'opt7': '002', 'type': 'comp'}, follow=True)
        self.assertTrue('KHARKOV-K13 PON 1/1/04/04:60.1.2' in response.content)
        self.assertTrue('Domain=00:02:9b:30:bf:5d' in response.content)
        self.assertTrue('<input type="hidden" name="login_del" value="KHARKOV-K13 PON 1/1/04/04:60.1.2">' in response.content)
        self.assertTrue('<input type="submit" value="Delete" name="submit">' in response.content)
        self.assertTrue('<input type="submit" value="No" name="submit">' in response.content)

    def test_syntax_error_handling(self):
        """
        Should return 'Error: ' + ERROR_MSG
        """
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/', {'login_name': 'test', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: TEST Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'login_name': 'test', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'login_name': '', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'login_name': 'KHaRKV-k05 PoN 1/1/01/1:01.1.1', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: KHARKV-K05 PON 1/1/01/1:01.1.1 Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'login_name': 'KHaRKoV-x09 PoN 1/1/01/1:01.1.1', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: KHARKOV-X09 PON 1/1/01/1:01.1.1 Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'login_name': 'KHaRKoV-x00 1/1/01/1:01.1.1', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: KHARKOV-X00 1/1/01/1:01.1.1 Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'login_name': 'не латин', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: НЕ ЛАТИН Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                              'opt1': 'err_val', 'opt2': '1', 'opt3': '01', 'opt4': '01', 'opt5': '1',
                                              'opt6': '1', 'opt7': '99', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                              'opt1': '1', 'opt2': 'err_val', 'opt3': '01', 'opt4': '01', 'opt5': '1',
                                              'opt6': '1', 'opt7': '99', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                              'opt1': '01', 'opt2': '1', 'opt3': 'err_val', 'opt4': '01', 'opt5': '1',
                                              'opt6': '1', 'opt7': '99', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                              'opt1': '01', 'opt2': '1', 'opt3': '01', 'opt4': 'err_val', 'opt5': '1',
                                              'opt6': '1', 'opt7': '99', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                              'opt1': '01', 'opt2': '1', 'opt3': '01', 'opt4': '01', 'opt5': 'err_val',
                                              'opt6': '1', 'opt7': '99', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                              'opt1': '01', 'opt2': '1', 'opt3': '01', 'opt4': '01', 'opt5': '1',
                                              'opt6': 'err_val', 'opt7': 'error_value', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                              'opt1': '01', 'opt2': '1', 'opt3': '01', 'opt4': '01', 'opt5': '1',
                                              'opt6': '1', 'opt7': 'err_val', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                              'opt1': '01', 'opt2': '1', 'opt3': '01', 'opt4': '01', 'opt5': '1',
                                              'opt6': '1', 'opt7': 'err_val', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

    def syntax_error_handling_xml(self):
        """
        Should return 'Error: ' + ERROR_MSG
        """
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/xml/', {'login_name': 'test', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: TEST Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'login_name': 'test', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'login_name': '', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'login_name': 'KHaRKV-k05 PoN 1/1/01/1:01.1.1', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: KHARKV-K05 PON 1/1/01/1:01.1.1 Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'login_name': 'KHaRKoV-x09 PoN 1/1/01/1:01.1.1', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: KHARKOV-X09 PON 1/1/01/1:01.1.1 Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'login_name': 'KHaRKoV-x00 1/1/01/1:01.1.1', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: KHARKOV-X00 1/1/01/1:01.1.1 Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'login_name': 'не латин', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: НЕ ЛАТИН Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                                  'opt1': 'err_val', 'opt2': '1', 'opt3': '01', 'opt4': '01', 'opt5': '1',
                                                  'opt6': '1', 'opt7': '99', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                                  'opt1': '1', 'opt2': 'err_val', 'opt3': '01', 'opt4': '01', 'opt5': '1',
                                                  'opt6': '1', 'opt7': '99', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                                  'opt1': '01', 'opt2': '1', 'opt3': 'err_val', 'opt4': '01', 'opt5': '1',
                                                  'opt6': '1', 'opt7': '99', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                                  'opt1': '01', 'opt2': '1', 'opt3': '01', 'opt4': 'err_val', 'opt5': '1',
                                                  'opt6': '1', 'opt7': '99', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                                  'opt1': '01', 'opt2': '1', 'opt3': '01', 'opt4': '01', 'opt5': 'err_val',
                                                  'opt6': '1', 'opt7': '99', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                                  'opt1': '01', 'opt2': '1', 'opt3': '01', 'opt4': '01', 'opt5': '1',
                                                  'opt6': 'err_val', 'opt7': 'error_value', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                                  'opt1': '01', 'opt2': '1', 'opt3': '01', 'opt4': '01', 'opt5': '1',
                                                  'opt6': '1', 'opt7': 'err_val', 'type': 'comp'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

        response = self.client.post('/ssc/xml/', {'city': 'KHARKOV', 'point': 'X00', 'login_name': '',
                                                  'opt1': '01', 'opt2': '1', 'opt3': '01', 'opt4': '01', 'opt5': '1',
                                                  'opt6': '1', 'opt7': 'err_val', 'type': 'raw'}, follow=True)
        self.assertTrue('Error: Incorrect input/Syntax error.' in response.content)

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

    #TODO stub make_request
    def test_logic(self):
        """
        Testing common logic.
        """
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKoV-x00 PoN 1/1/01/01:1.1.99'}, follow=True)
        self.assertEqual(response.content, '[["No sessions were found which matched the search criteria."], false]')

        response = self.client.post('/ssc/ajax/', {'login_name': 'KHARKOV-K13 PON 1/1/04/04:60.1.2'}, follow=True)
        self.assertTrue('KHARKOV-K13 PON 1/1/04/04:60.1.2' in response.content)
        self.assertTrue('Domain=00:02:9b:30:bf:5d' in response.content)

    #TODO stub return value
    def test_logic_xml(self):
        """
        Testing logic.
        """
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/ajax/xml/', {'login_name': 'KHaRKoV-x00 PoN 1/1/01/01:1.1.99'}, follow=True)
        self.assertEqual(response.content, '[["No sessions were found which matched the search criteria."], false]')

        response = self.client.post('/ssc/ajax/xml/', {'login_name': 'KHARKOV-K13 PON 1/1/04/04:60.1.2'}, follow=True)
        self.assertTrue('KHARKOV-K13 PON 1/1/04/04:60.1.2' in response.content)
        self.assertTrue('Domain=00:02:9b:30:bf:5d' in response.content)

    def test_syntax_error_handling(self):
        """
        Should return 'Error: ' + ERROR_MSG
        """
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/ajax/', {}, follow=True)
        self.assertEqual(response.content, '[["Error: Incorrect input/Syntax error."], false]')

        response = self.client.post('/ssc/ajax/', {'login_name': 'test'}, follow=True)
        self.assertEqual(response.content, '[["Error: TEST Incorrect input/Syntax error."], false]')

        response = self.client.post('/ssc/ajax/', {'login_name': ''}, follow=True)
        self.assertEqual(response.content, '[["Error: Incorrect input/Syntax error."], false]')

        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKV-k05 PoN 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, '[["Error: KHARKV-K05 PON 1/1/01/1:01.1.1 Incorrect input/Syntax error."], false]')

        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKoV-x09 PoN 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, '[["Error: KHARKOV-X09 PON 1/1/01/1:01.1.1 Incorrect input/Syntax error."], false]')

        response = self.client.post('/ssc/ajax/', {'login_name': 'KHaRKoV-x09 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, '[["Error: KHARKOV-X09 1/1/01/1:01.1.1 Incorrect input/Syntax error."], false]')

        #response = self.client.post('/ssc/ajax/', {'login_name': 'не латин'}, follow=True)
        #self.assertEqual(response.content, [["Error: НЕ ЛАТИН Incorrect input/Syntax error."], false]')

    def test_syntax_error_handling_xml(self):
        """
        Should return 'Error: ' + ERROR_MSG
        """
        self.client.login(username='max', password='test')

        response = self.client.post('/ssc/ajax/xml/', {}, follow=True)
        self.assertEqual(response.content, '[["Error: Incorrect input/Syntax error."], false]')

        response = self.client.post('/ssc/ajax/xml/', {'login_name': 'test'}, follow=True)
        self.assertEqual(response.content, '[["Error: TEST Incorrect input/Syntax error."], false]')

        response = self.client.post('/ssc/ajax/xml/', {'login_name': ''}, follow=True)
        self.assertEqual(response.content, '[["Error: Incorrect input/Syntax error."], false]')

        response = self.client.post('/ssc/ajax/xml/', {'login_name': 'KHaRKV-k05 PoN 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, '[["Error: KHARKV-K05 PON 1/1/01/1:01.1.1 Incorrect input/Syntax error."], false]')

        response = self.client.post('/ssc/ajax/xml/', {'login_name': 'KHaRKoV-x09 PoN 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, '[["Error: KHARKOV-X09 PON 1/1/01/1:01.1.1 Incorrect input/Syntax error."], false]')

        response = self.client.post('/ssc/ajax/xml/', {'login_name': 'KHaRKoV-x09 1/1/01/1:01.1.1'}, follow=True)
        self.assertEqual(response.content, '[["Error: KHARKOV-X09 1/1/01/1:01.1.1 Incorrect input/Syntax error."], false]')

        #response = self.client.post('/ssc/ajax/xml/', {'login_name': 'не латин'}, follow=True)
        #self.assertEqual(response.content, [["Error: НЕ ЛАТИН Incorrect input/Syntax error."], false]')
