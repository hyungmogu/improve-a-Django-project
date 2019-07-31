import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import (Ingredient, Item, Menu)


# VIEW TEST
class MenuListPageTestCase(TestCase):
    '''Tests for the Home page view'''
    def setUp(self):
        self.menu1 = Menu.objects.create(
            season='Season 1'
        )

        self.menu2 = Menu.objects.create(
            season='Season 2',
            expiration_date=datetime.datetime(
                2019, 8, 23,
                tzinfo=timezone.utc)
        )

        self.menu3 = Menu.objects.create(
            season='Season 3',
            expiration_date=datetime.datetime(
                2019, 4, 23,
                tzinfo=timezone.utc)
        )

        self.resp = self.client.get('/')

    def test_return_status_okay(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_return_none_expired_menu_on_home_page(self):
        expected_length = 2

        result_length = len(self.resp.context['menus'])

        self.assertEqual(expected_length, result_length)

    def test_return_layoutHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'menu/layout.html')

    def test_return_homeHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'menu/home.html')

