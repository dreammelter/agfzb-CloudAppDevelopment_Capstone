from django.http import response
from django.test import TestCase
from django.test.testcases import SimpleTestCase

# Create your tests here.
class StatusCodeTests(SimpleTestCase):
    """
    Verify the we get the expected response codes (200 or redirect) for each page/route
    """
    # Test Responses for Static Pages:
    def test_no_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 301) # should be a permanent redirect

    def test_index_page_status(self):
        response = self.client.get('/djangoapp/')
        self.assertEqual(response.status_code, 200)

    def test_about_page_status(self):
        response = self.client.get('/djangoapp/about/')
        self.assertEqual(response.status_code, 200)

    def test_contact_page_status(self):
        response = self.client.get('/djangoapp/contact/')
        self.assertEqual(response.status_code, 200)