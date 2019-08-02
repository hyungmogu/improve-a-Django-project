import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import (Ingredient, Item, Menu)
from .forms import MenuForm


# MODEL TEST
class IngredientModelTestCase(TestCase):
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


# FORM TEST
class MenuFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('moe', 'moe@example.com', '12345')
        self.item1 = Item.objects.create(
            name='Omelette',
            description='Is a delicious stuff',
            chef=self.user,
            standard=True
        )

        self.item2 = Item.objects.create(
            name='Spaghetti',
            description='this may be a delicious stuff',
            chef=self.user,
            standard=True
        )

    def test_return_form_invalid_if_season_name_is_not_filled(self):
        expected = False

        form = MenuForm({
            'items': ['1','2'],
            'expiration_date': '06/12/2019'
        })

        result = form.is_valid()

        self.assertEqual(expected, result)

    def test_return_form_invalid_if_item_selected_is_empty(self):
        expected = False

        form = MenuForm({
            'season': 'hello',
            'expiration_date': '06/12/2019'
        })

        result = form.is_valid()

        self.assertEqual(expected, result)

    def test_return_form_invalid_if_date_is_not_filled(self):
        expected = False

        form = MenuForm({
            'season': 'hello',
            'items': ['1','2']
        })

        result = form.is_valid()

        self.assertEqual(expected, result)

    def test_return_form_invalid_if_date_format_is_not_MMDDYYYY(self):
        expected = False

        form1 = MenuForm({
            'season': 'hello',
            'items': ['1','2'],
            'expiration_date': '31/12/2019'
        })

        result1 = form1.is_valid()

        form2 = MenuForm({
            'season': 'hello',
            'items': ['1','2'],
            'expiration_date': '2019/12/31'
        })

        result2 = form2.is_valid()


        form3 = MenuForm({
            'season': 'hello',
            'items': ['1','2'],
            'expiration_date': '31-12-2019'
        })

        result3 = form3.is_valid()

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_form_valid_when_all_are_correct(self):
        expected = True

        form = MenuForm(data={
            'season': 'hello',
            'items': ['1','2'],
            'expiration_date': '06/12/2019'
        })
        result = form.is_valid()

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

    def test_return_status_404_if_menu_not_found(self):
        expected = 404

        temp = self.client.get('/menu/1000/')
        result = temp.status_code

        self.assertEqual(expected, result)

    def test_return_layoutHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'menu/layout.html')

    def test_return_menuDetailHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'menu/menu_detail.html')

    def test_return_menu1_on_visit(self):
        self.assertContains(self.resp, self.menu1.season)

    def test_return_only_one_item_on_visit(self):
        self.assertNotContains(self.resp, self.menu2.season)


class ItemDetailPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('moe', 'moe@example.com', '12345')

        self.item1 = Item.objects.create(
            name='Omelette',
            description='Is a delicious stuff',
            chef=self.user,
            standard=True
        )

        self.item2 = Item.objects.create(
            name='Spaghetti',
            description='this may be a delicious stuff',
            chef=self.user,
            standard=True
        )

        self.resp = self.client.get('/menu/item/{0}/'.format(self.item1.pk))

    def test_return_status_okay(self):
        expected = 200

        result = self.resp.status_code

        self.assertEqual(result, expected)

    def test_return_status_404_if_item_not_found(self):
        expected = 404

        temp = self.client.get('/menu/item/1000/')
        result = temp.status_code

        self.assertEqual(expected, result)

    def test_return_layoutHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'menu/layout.html')

    def test_return_itemDetailHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'menu/item_detail.html')

    def test_return_item1_on_visit(self):
        self.assertContains(self.resp, self.item1.name)

    def test_return_only_one_item_on_visit(self):
        self.assertNotContains(self.resp, self.item2.name)


class CreateNewMenuPageTestCase(TestCase):
    def setUp(self):
        self.resp = self.client.get('/menu/new/')

    def test_return_status_okay_if_logged_in(self):
        expected = 200

        User.objects.create_user('moe', 'moe@example.com', '12345')
        self.client.login(username='moe', password='12345')
        response = self.client.get(reverse('menu_new'))
        result = response.status_code

        self.assertEqual(result, expected)

    # def test_404_if_not_logged_in(self):
    #     expected = 404

    #     response = self.client.get(reverse('menu_new'))
    #     result = response.status_code

    #     self.assertEqual(expected, result)

    def test_return_layoutHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'menu/layout.html')

    def test_return_itemDetailHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'menu/menu_create.html')


class CreateNewMenuPagePOSTRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('moe', 'moe@example.com', '12345')
        self.item1 = Item.objects.create(
            name='Omelette',
            description='Is a delicious stuff',
            chef=self.user,
            standard=True
        )

        self.item2 = Item.objects.create(
            name='Spaghetti',
            description='this may be a delicious stuff',
            chef=self.user,
            standard=True
        )

    def test_return_menu_detail_page_if_successful(self):
        response = self.client.post('/menu/new/', {
            'season': 'hello',
            'items': ['1','2'],
            'expiration_date': '06/12/2019'
        })

        self.assertRedirects(response, reverse('menu_detail', kwargs={'pk': 1,}), fetch_redirect_response=False)

    def test_return_menu_with_length_1_if_successful(self):
        expected = 1

        response = self.client.post('/menu/new/',  {
            'season': 'hello',
            'items': ['1','2'],
            'expiration_date': '06/12/2019'
        })

        result = Menu.objects.all().count()

        self.assertEqual(expected, result)

    def test_return_menu_create_page_if_not_successful(self):
        expected = 'New Menu'

        response = self.client.post('/menu/new/',  {
            'season': 'hello',
            'items': ['1','2'],
            'expiration_date': '06-12-2019'
        })

        self.assertContains(response, expected)
