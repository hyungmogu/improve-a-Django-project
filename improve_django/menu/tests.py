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


class MenuModelTestCase(TestCase):
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

        self.item3 = Item.objects.create(
            name='Steak',
            description='this could be a delicious food',
            chef=self.user,
            standard=True
        )

        self.menu1 = Menu.objects.create(
            season='Menu 1',
            expiration_date=datetime.datetime(
                2019, 8, 23,
                tzinfo=timezone.utc)
        )
        self.menu1.items.add(self.item1)
        self.menu1.items.add(self.item2)

        self.menu2 = Menu.objects.create(
            season='Menu 1',
            expiration_date=datetime.datetime(
                2019, 8, 23,
                tzinfo=timezone.utc)
        )
        self.menu2.items.add(self.item1)
        self.menu2.items.add(self.item3)


    def test_return_table_length_of_2(self):
        expected = 2

        result = Menu.objects.count()

        self.assertEqual(expected, result)

    def test_return_menu_1_given_pk_of_1(self):
        expected = 'Menu 1'

        menu = Menu.objects.get(pk=1)
        result = menu.season

        self.assertEqual(expected, result)

    def test_return_pk_1_with_08232019_as_exp_date(self):
        expected = '08/23/2019'

        menu = Menu.objects.get(pk=1)
        result = menu.expiration_date.strftime('%m/%d/%Y')

        self.assertEqual(expected, result)

    def test_return_pk_1_with_length_of_2_for_items(self):
        expected = 2

        menu = Menu.objects.get(pk=1)
        result = menu.items.count()

        self.assertEqual(expected, result)

    def test_return_name_when_type_casted_with_str(self):
        expected = 'Menu 1'

        menu = Menu.objects.get(pk=1)
        result = str(menu)

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
        self.assertTemplateUsed(self.resp, 'layout.html')

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
        self.assertTemplateUsed(self.resp, 'layout.html')

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
        self.assertTemplateUsed(self.resp, 'layout.html')

    def test_return_itemDetailHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'menu/item_detail.html')

    def test_return_item1_on_visit(self):
        self.assertContains(self.resp, self.item1.name)

    def test_return_only_one_item_on_visit(self):
        self.assertNotContains(self.resp, self.item2.name)


class CreateNewMenuPageGETRequestTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('moe', 'moe@example.com', '12345')

    def test_return_status_okay_if_logged_in(self):
        expected = 200

        self.client.login(username='moe', password='12345')
        response = self.client.get(reverse('menu_new'))
        result = response.status_code

        self.assertEqual(result, expected)

    def test_return_status_code_302_if_not_logged_in(self):
        expected = 302

        response = self.client.get(reverse('menu_new'))
        result = response.status_code

        self.assertEqual(expected, result)

    def test_return_layoutHtml_as_template_used_if_logged_in(self):
        self.client.login(username='moe', password='12345')
        response = self.client.get(reverse('menu_new'))
        self.assertTemplateUsed(response, 'layout.html')

    def test_return_itemDetailHtml_as_template_used_if_logged_in(self):
        self.client.login(username='moe', password='12345')
        response = self.client.get(reverse('menu_new'))
        self.assertTemplateUsed(response, 'menu/menu_create.html')


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

    def test_return_status_302_if_user_not_logged_in(self):
        expected = 302

        response = self.client.post('/menu/new/', {
            'season': 'hello',
            'items': ['1','2'],
            'expiration_date': '06/12/2019'
        })

        result = response.status_code

        self.assertEqual(expected, result)

    def test_return_menu_detail_page_if_successful(self):
        self.client.login(username='moe', password='12345')
        response = self.client.post('/menu/new/', {
            'season': 'hello',
            'items': ['1','2'],
            'expiration_date': '06/12/2019'
        })

        self.assertRedirects(response, reverse('menu_detail', kwargs={'pk': 1,}), fetch_redirect_response=False)

    def test_return_menu_with_length_1_if_successful(self):
        expected = 1

        self.client.login(username='moe', password='12345')
        response = self.client.post('/menu/new/',  {
            'season': 'hello',
            'items': ['1','2'],
            'expiration_date': '06/12/2019'
        })

        result = Menu.objects.all().count()

        self.assertEqual(expected, result)

    def test_retrun_menu_with_season_hi_if_successful(self):
        expected = 'hi'

        self.client.login(username='moe', password='12345')
        self.client.post('/menu/new/', {
            'season': 'hi',
            'items': ['1','2'],
            'expiration_date': '06/11/2019'
        })

        menu = Menu.objects.get(pk=1)
        result = menu.season

        self.assertEqual(expected, result)

    def test_return_menu_with_exp_date_06112019_if_successful(self):
        expected = '06/11/2019'

        self.client.login(username='moe', password='12345')
        self.client.post('/menu/new/', {
            'season': 'hi',
            'items': ['1','2'],
            'expiration_date': '06/11/2019'
        })

        menu = Menu.objects.get(pk=1)
        result = menu.expiration_date.strftime("%m/%d/%Y")

        self.assertEqual(expected, result)


    def test_return_menu_with_items_of_length_2_if_successful(self):
        expected = 2

        self.client.login(username='moe', password='12345')
        self.client.post('/menu/new/', {
            'season': 'hi',
            'items': ['1','2'],
            'expiration_date': '06/11/2019'
        })

        menu = Menu.objects.get(pk=1)
        result = menu.items.count()

        self.assertEqual(expected, result)

    def test_return_menu_create_page_if_not_successful(self):
        expected = 'New Menu'

        self.client.login(username='moe', password='12345')
        response = self.client.post('/menu/new/',  {
            'season': 'hello',
            'items': ['1','2'],
            'expiration_date': '06-12-2019'
        })

        self.assertContains(response, expected)


class EditMenuPageGETRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('moe', 'moe@example.com', '12345')
        self.menu1 = Menu.objects.create(
            season='Menu 1',
            expiration_date=datetime.datetime(
                2019, 8, 23,
                tzinfo=timezone.utc)
        )

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

    def test_return_status_okay_if_logged_in(self):
        expected = 200

        self.client.login(username='moe', password='12345')
        response = self.client.get(reverse('menu_edit', kwargs={'pk': 1}))
        result = response.status_code

        self.assertEqual(result, expected)

    def test_return_302_if_not_logged_in(self):
        expected = 302

        response = self.client.get(reverse('menu_new'))
        result = response.status_code

        self.assertEqual(expected, result)

    def test_return_layoutHtml_as_template_used_if_logged_in(self):
        expected = 'layout.html'

        self.client.login(username='moe', password='12345')
        response = self.client.get(reverse('menu_edit', kwargs={'pk': 1}))

        self.assertTemplateUsed(response, expected)

    def test_return_itemDetailHtml_as_template_used_if_logged_in(self):
        expected= 'menu/menu_edit.html'

        self.client.login(username='moe', password='12345')
        response = self.client.get(reverse('menu_edit', kwargs={'pk': 1}))

        self.assertTemplateUsed(response, expected)


class EditMenuPagePOSTRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('moe', 'moe@example.com', '12345')
        self.menu1 = Menu.objects.create(
            season='Menu 1',
            expiration_date=datetime.datetime(
                2019, 8, 23,
                tzinfo=timezone.utc)
        )

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

    def test_return_302_if_not_logged_in(self):
        expected = 302

        response = self.client.post('/menu/1/edit/', {
            'season': 'hi',
            'items': ['1','2'],
            'expiration_date': '06/11/2019'
        })
        result = response.status_code

        self.assertEqual(expected, result)


    def test_return_back_to_menu_edit_page_if_successful(self):
        expected = 'Edit Menu'

        self.client.login(username='moe', password='12345')
        response = self.client.post('/menu/1/edit/', {
            'season': 'hi',
            'items': ['1','2'],
            'expiration_date': '06/11/2019'
        })

        self.assertContains(response, expected)

    def test_retrun_menu_with_season_hi_if_edit_successful(self):
        expected = 'hi'

        self.client.login(username='moe', password='12345')
        self.client.post('/menu/1/edit/', {
            'season': 'hi',
            'items': ['1','2'],
            'expiration_date': '06/11/2019'
        })

        menu = Menu.objects.get(pk=1)
        result = menu.season

        self.assertEqual(expected, result)

    def test_return_menu_with_exp_date_06112019_if_edit_successful(self):
        expected = '06/11/2019'

        self.client.login(username='moe', password='12345')
        self.client.post('/menu/1/edit/', {
            'season': 'hi',
            'items': ['1','2'],
            'expiration_date': '06/11/2019'
        })

        menu = Menu.objects.get(pk=1)
        result = menu.expiration_date.strftime("%m/%d/%Y")

        self.assertEqual(expected, result)


    def test_return_menu_with_items_of_length_2_if_edit_successful(self):
        expected = 2

        self.client.login(username='moe', password='12345')
        self.client.post('/menu/1/edit/', {
            'season': 'hi',
            'items': ['1','2'],
            'expiration_date': '06/11/2019'
        })

        menu = Menu.objects.get(pk=1)
        result = menu.items.count()

        self.assertEqual(expected, result)

    def test_return_back_to_menu_edit_page_if_loggedin_and_not_successful(self):
        expected = 'Edit Menu'

        self.client.login(username='moe', password='12345')
        response = self.client.post('/menu/1/edit/', {
            'season': 'hi',
            'items': ['1','2'],
            'expiration_date': '31-12-2019'
        })

        self.assertContains(response, expected)


class ItemListPageTestCase(TestCase):
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

        self.resp = self.client.get('/menu/item/')

    def test_return_status_okay(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_return_length_2_as_number_of_items_on_page(self):
        expected_length = 2

        result_length = len(self.resp.context['items'])

        self.assertEqual(expected_length, result_length)

    def test_return_layoutHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'layout.html')

    def test_return_itemListHtml_as_template_used(self):
        self.assertTemplateUsed(self.resp, 'menu/item_list.html')


"""

TESTS FOR EDIT
    GET Request
        [x]: should return status 200
        [x]: When on page, layout.html should be used
        [x]: When on page, item_edit.html should be used
    POST Request
        [x]: When successful, the changed info should be reflected accordingly
        [x]: When successful, user should be redirected to item detail page
        [x]: When not successful, user should stay on the same page
"""
class EditItemPageGETRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('moe', 'moe@example.com', '12345')

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

        self.item1 = Item.objects.create(
            name='Omelette',
            description='this is a delicious stuff',
            chef=self.user,
            standard=True
        )

        self.item1.ingredients.add(self.ingredient1)
        self.item1.ingredients.add(self.ingredient2)
        self.item1.ingredients.add(self.ingredient3)
        self.item1.ingredients.add(self.ingredient4)

    def test_return_status_okay_if_logged_in(self):
        expected = 200

        self.client.login(username='moe', password='12345')
        response = self.client.get(reverse('item_edit', kwargs={'pk': 1}))
        result = response.status_code

        self.assertEqual(result, expected)

    def test_return_302_if_not_logged_in(self):
        expected = 302

        response = self.client.get(reverse('item_edit', kwargs={'pk': 1}))
        result = response.status_code

        self.assertEqual(expected, result)

    def test_return_layoutHtml_as_template_used_if_logged_in(self):
        expected = 'layout.html'

        self.client.login(username='moe', password='12345')
        response = self.client.get(reverse('item_edit', kwargs={'pk': 1}))

        self.assertTemplateUsed(response, expected)

    def test_return_itemEditHtml_as_template_used_if_logged_in(self):
        expected= 'menu/item_edit.html'

        self.client.login(username='moe', password='12345')
        response = self.client.get(reverse('item_edit', kwargs={'pk': 1}))

        self.assertTemplateUsed(response, expected)


class EditItemPagePOSTRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('moe', 'moe@example.com', '12345')

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

        self.item1 = Item.objects.create(
            name='Omelette',
            description='this is a delicious stuff',
            chef=self.user,
            standard=True
        )

        self.item1.ingredients.add(self.ingredient1)
        self.item1.ingredients.add(self.ingredient2)
        self.item1.ingredients.add(self.ingredient3)
        self.item1.ingredients.add(self.ingredient4)

    def test_return_302_if_try_to_edit_while_not_logged_in(self):
        expected = 302

        response = self.client.post(reverse('item_edit', kwargs={'pk':1}), {
            'name': 'Scrambled Egg',
            'ingredients': ['2','3'],
            'description':'this is a delicious stuff',
            'chef':['1'],
            'standard':True
        })
        result = response.status_code

        self.assertEqual(expected, result)

    def test_return_login_page_if_try_to_edit_while_not_logged_in(self):
        expected = 'accounts/sign_in.html'

        response = self.client.post(reverse('item_edit', kwargs={'pk':1}), {
            'name': 'Scrambled Egg',
            'ingredients': ['2','3'],
            'description':'this is a delicious stuff',
            'chef':['1'],
            'standard':True
        }, follow=True)

        self.assertTemplateUsed(response, expected)


    def test_retrun_item_with_name_scrambled_egg_if_edit_successful(self):
        expected = 'Scrambled Egg'

        self.client.login(username='moe', password='12345')
        self.client.post(reverse('item_edit', kwargs={'pk':1}), {
            'name': 'Scrambled Egg',
            'ingredients': ['2','3'],
            'description':'this is a delicious stuff',
            'chef':['1'],
            'standard':True
        })

        item = Item.objects.get(pk=1)
        result = item.name

        self.assertEqual(expected, result)


    def test_return_item_with_ingredients_of_length_2_if_edit_successful(self):
        expected = 2

        self.client.login(username='moe', password='12345')
        self.client.post(reverse('item_edit', kwargs={'pk':1}), {
            'name': 'Scrambled Egg',
            'ingredients': ['2','3'],
            'description':'this is a delicious stuff',
            'chef':['1'],
            'standard':True
        })

        item = Item.objects.get(pk=1)
        result = item.ingredients.count()

        self.assertEqual(expected, result)

    def test_return_item_with_chef_laceywill_if_edit_successful(self):
        expected = 'laceywill'

        self.client.login(username='moe', password='12345')
        self.client.post(reverse('item_edit', kwargs={'pk':1}), {
            'name': 'Scrambled Egg',
            'ingredients': ['2','3'],
            'description':'this is a delicious stuff',
            'chef':['1'],
            'standard':True
        })

        item = Item.objects.get(pk=1)
        result = item.chef.username

        self.assertEqual(expected, result)

    def test_return_item_with_standard_as_true_if_edit_successful(self):
        expected = True

        self.client.login(username='moe', password='12345')
        self.client.post(reverse('item_edit', kwargs={'pk':1}), {
            'name': 'Scrambled Egg',
            'ingredients': ['2','3'],
            'description':'this is a delicious stuff',
            'chef':['2'],
            'standard':True
        })

        item = Item.objects.get(pk=1)
        result = item.standard

        self.assertEqual(expected, result)

    def test_return_back_to_item_detail_page_if_edit_successful(self):
        expected = 'menu/item_detail.html'

        self.client.login(username='moe', password='12345')
        response = self.client.post(reverse('item_edit', kwargs={'pk':1}), {
            'name': 'Scrambled Egg',
            'ingredients': ['2','3'],
            'description':'this is a delicious stuff',
            'chef':['1'],
            'standard':True
        }, follow=True)

        self.assertTemplateUsed(response, expected)


    def test_return_item_edit_page_if_edit_not_successful(self):
        expected = 'menu/item_edit.html'

        self.client.login(username='moe', password='12345')
        response = self.client.post(reverse('item_edit', kwargs={'pk':1}), {
            'name': 'Scrambled Egg',
            'ingredients': ['2','3'],
            'description':'this is a delicious stuff',
            'chef':2,
            'standard':True
        }, follow=True)

        self.assertTemplateUsed(response, expected)