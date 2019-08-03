"""
TODO LIST FOR ACCOUNTS APP (TESTS)

[]: 1) Add test for user model
    - given 2 users, with 1 of format {username:"hello", password: "hello"}, and the other
    {username: "world", password: "world"},
        []: user model returns query count of 2
        []: user model with pk == 1 has name "hello" and password "hello"
        []: user model with pk == 2 has name "world" and password "hello"
        []: type casting a queried item returns username

[x]: 2) Add test for /accounts/login
    GET REQUEST
        [x]: returns status 200 (okay) on visit
        [x]: uses layout.html as template
        [x]: uses /accounts/sign_in.html as template

    POST REQUEST
        [x]: When not successful and password is incorrect, user is sent back to sign_in page
        [x]: When not successful, and username is incorrect, user is sent back to sign_in_page
        [x]: When successful, user is redirected to home page

[x]: 3) Add test for /accounts/sign_up
    GET REQUEST
        [x]: returns status 200 on visit
        [x]: uses layout.html as template
        [x]: uses sign_up.html as template

    POST REQUEST
        [x]: When unsuccessful, user is sent back to sign up page
        [x]: When successful, message "You're now a user! You've been signed in, too." is returned
        [x]: When successful, user model has total query count of 1
        [x]: When successful, user is redirected to home page

[x]: 4) Add test for /accounts/logout
    [x]: When successful, user is redirected to home page
    [x]: When successful, message 'You've been signed out. Come back soon!' is returned

"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your tests here.

# VIEW TESTS
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


class SignUpGETRequestTestCase(TestCase):
    def setUp(self):
        self.resp = self.client.get(reverse('accounts:sign_up'))

    def test_returns_status_200_on_visit(self):
        expected = 200

        result = self.resp.status_code

        self.assertEqual(expected, result)

    def test_return_layoutHtml_as_template_used(self):
        expected = 'layout.html'

        self.assertTemplateUsed(self.resp, expected)

    def test_return_signinHtml_as_template_used(self):
        expected = 'accounts/sign_up.html'

        self.assertTemplateUsed(self.resp, expected)


class SignUpPOSTRequestTestCase(TestCase):
    def setUp(self):
        self.resp = self.client.post(reverse('accounts:sign_up'), {
            'username': 'hello',
            'password1': 'hello1',
            'password2': 'hello1'
        })

    def test_return_to_sign_up_page_if_signup_unsuccessful(self):
        expected = 'accounts/sign_up.html'

        response1 = self.client.post(reverse('accounts:sign_up'), {
            'username': 'hello',
            'password1': 'hello1',
            'password2': 'hello2'
        })

        response2 = self.client.post(reverse('accounts:sign_up'), {
            'username': 'hel lo',
            'password1': 'hello1',
            'password2': 'hello1'
        })


        self.assertTemplateUsed(response1, expected)
        self.assertTemplateUsed(response2, expected)

    def test_return_message_if_signup_successful(self):
        expected = "You're now a user! You've been signed in, too."

        response = self.client.post(reverse('accounts:sign_up'), {
            'username': 'hello',
            'password1': 'hello1',
            'password2': 'hello1'
        }, follow=True)

        messages = list(response.context['messages'])
        result = str(messages[0])

        self.assertEqual(expected, result)

    def test_return_user_model_with_count_of_1_if_signup_successful(self):
        expected = 1

        result = User.objects.all().count()

        self.assertEqual(expected, result)

    def test_return_to_home_page_if_signup_successful(self):
        self.assertRedirects(self.resp, reverse('home'), fetch_redirect_response=False)


class LogoutPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('hello', 'hello@example.com', 'hello')
        self.res_login = self.client.post(reverse('accounts:login'), {
            'username': 'hello',
            'password': 'hello'
        })

        self.res_logout = self.client.get(reverse('accounts:logout'))

    def test_return_status_302_if_logout_successful(self):
        expected = 302

        result = self.res_logout.status_code

        self.assertEqual(expected, result)

    def test_return_home_page_if_logout_successful(self):
        self.assertRedirects(self.res_logout, reverse('home'), fetch_redirect_response=False)

    def test_return_message_if_logout_successful(self):
        expected = "You've been signed out. Come back soon!"

        response = self.client.get(reverse('accounts:logout'), follow=True) # follow necesary to see messages
        messages = list(response.context['messages'])
        result = str(messages[0])

        self.assertEqual(expected, result)