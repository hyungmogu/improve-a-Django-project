"""
TODO LIST FOR ACCOUNTS APP (TESTS)

[]: 1) Add test for user model

[]: 2) Add test for /accounts/login
    GET REQUEST
        [x]: returns status 200 (okay) on visit
        [x]: uses layout.html as template
        [x]: uses /accounts/sign_in.html as template

    POST REQUEST
        [x]: if not successful and password is incorrect, user is sent back to sign_in page
        [x]: if not successful, username is incorrect, user is sent back to sign_in_page
        [x]: if successful, user is redirected to home page

[]: 3) Add test for /accounts/sign_up

[]: 4) Add test for /accounts/logout
    []:

"""
from django.test import TestCase
from django.contrib.auth.models import User
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


class LoginPagePOSTRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('hello', 'hello@example.com', 'hello')

    def test_return_status_302_if_login_successful(self):
        expected = 302

        response = self.client.post(reverse('accounts:login'), {
            'username': 'hello',
            'password': 'hello'
        })
        result = response.status_code

        self.assertEqual(expected, result)

    def test_return_home_page_if_login_successful(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'hello',
            'password': 'hello'
        })
        self.assertRedirects(response, reverse('home'), fetch_redirect_response=False)


    def test_return_sign_in_page_if_password_incorrect(self):

        response = self.client.post(reverse('accounts:login'), {
            'username': 'hello',
            'password': 'hello2'
        })

        self.assertTemplateUsed(response, 'layout.html')
        self.assertTemplateUsed(response, 'accounts/sign_in.html')


    def test_return_sign_in_page_if_username_incorrect(self):

        response = self.client.post(reverse('accounts:login'), {
            'username': 'hello4',
            'password': 'hello'
        })

        self.assertTemplateUsed(response, 'layout.html')
        self.assertTemplateUsed(response, 'accounts/sign_in.html')
