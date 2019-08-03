"""
TODO LIST FOR ACCOUNTS APP (TESTS)

[]: 1) Add test for user model
    []:

[]: 2) Add test for /accounts/login
    GET REQUEST
        [x]: returns status 200 (okay) on visit
        [x]: uses layout.html as template
        [x]: uses /accounts/sign_in.html as template

    POST REQUEST
        []: if not successful and password is incorrect, user is sent back to sign_in page
        []: if not successful and password is incorrect, user is shown error message 'Username or password is incorrect.'
        []: if not successful and password is correct, user is sent back to sign_in page
        []: if not successful and password is correct, user is shown error message 'username or password is incorrect'
        []: if successful, user is redirected to home page

[]: 3) Add test for /accounts/sign_up

[]: 4) Add test for /accounts/logout
    []:

"""
from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here.

class LoginPageGETRequestTestCase(TestCase):
    def setUp(self):
        self.resp = self.client.get(reverse('accounts:login'))

    def test_return_status_200_on_visit(self):
        expected = 200

        result = self.resp.status_code

        self.assertEqual(expected, result)

    def test_return_layoutHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'layout.html')

    def test_return_sign_inHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'accounts/sign_in.html')


