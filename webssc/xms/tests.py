from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


class XmsTestCase(TestCase):
    def setUp(self):
        """
        Preconditions
        """
        self.user = User.objects.create_user('test', 'test@mail.com', 'test')
        self.client = Client()

class XmsAuthTest(XmsTestCase):
    """
    Testing for access to page for logged user
    and not.
    """
    def test_unauthorized_acces(self):
        """
        Should redirect to login page if not
        authentificated xms/.
        """
        response = self.client.get('/xms/', follow=True)
        self.assertEqual(response.templates[0].name, 'xms/login.html')

    def test_rendering_xms_page(self):
        """
        Should render xms.html template /xms/.
        """
        self.client.login(username='test', password='test')

        response = self.client.get('/xms/', follow=True)
        self.assertEqual(response.templates[0].name, 'xms/default_xms.html')

class XmsTest(XmsTestCase):
    """
    Common test for default behaviour,
    for selecting different column, for sorting etc.
    """
    def test_default_rendering(self):
        """
        Should render all database content by default.
        """
        self.client.login(username='test', password='test')

        response = self.client.get('/xms/', follow=True)
        pass 
