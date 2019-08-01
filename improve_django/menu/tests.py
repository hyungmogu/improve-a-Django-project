import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import (Ingredient, Item, Menu)


# MODEL TEST
class IngredientModelTest(TestCase):
    def setUp(self):
        self.ingredient1 = Ingredient.objects.create(
            name='Salami'
        )

        self.ingredient2 = Ingredient.objects.create(
            name='Tomato'
        )

        self.ingredient3 = Ingredient.objects.create(
            name='Egg'
        )

        self.ingredient4 = Ingredient.objects.create(
            name='Cheddar Cheese'
        )

    def test_return_table_length_of_4(self):
        expected = 4

        result = Ingredient.objects.count()

        self.assertEqual(expected, result)

    def test_return_salami_given_pk_of_1(self):
        expected = 'Salami'

        ingredient = Ingredient.objects.get(pk=1)
        result = ingredient.name

        self.assertEqual(expected, result)

    def test_return_salami_given_pk_of_2(self):
        expected = 'Tomato'

        ingredient = Ingredient.objects.get(pk=2)
        result = ingredient.name

        self.assertEqual(expected, result)

    def test_return_egg_given_pk_of_3(self):
        expected = 'Egg'

        ingredient = Ingredient.objects.get(pk=3)
        result = ingredient.name

        self.assertEqual(expected, result)

    def test_return_egg_given_pk_of_4(self):
        expected = 'Cheddar Cheese'

        ingredient = Ingredient.objects.get(pk=4)
        result = ingredient.name

        self.assertEqual(expected, result)

    def test_return_name_when_type_casted_with_str(self):
        expected = 'Salami'

        ingredient = Ingredient.objects.get(pk=1)
        result = str(ingredient)

        self.assertEqual(expected, result)


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


class MenuDetailPageTestCase(TestCase):
    def setUp(self):
        self.menu1 = Menu.objects.create(
            season='Menu 1',
            expiration_date=datetime.datetime(
                2019, 8, 23,
                tzinfo=timezone.utc)
        )

        self.menu2 = Menu.objects.create(
            season='Menu 2',
            expiration_date=datetime.datetime(
                2019, 9, 21,
                tzinfo=timezone.utc)
        )

        self.resp = self.client.get('/menu/{0}/'.format(self.menu1.pk))

    def test_return_status_okay(self):
        expected = 200

        result = self.resp.status_code

        self.assertEqual(expected, result)

    def test_return_status_404(self):
        expected = 404

        temp = self.client.get('/menu/1000/')
        result = self.resp.status_code

        self.assertEqual(expected, result)

    def test_return_layoutHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'menu/layout.html')

    def test_return_menuDetailHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'menu/menu_detail.html')

    def test_return_menu1_on_visit(self):
        self.assertContains(self.resp, self.menu1.season)

    def test_return_only_one_item_on_visit(self):
        self.assertNotContains(self.resp, self.menu2.season)
