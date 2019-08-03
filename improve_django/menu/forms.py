from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects,
        error_messages={'required': 'Please select at least one item'},
        widget=forms.SelectMultiple(attrs={'class': 'width-100'})
    )

    expiration_date = forms.DateTimeField(
        error_messages={'invalid': 'Please enter date in the format MM/DD/YYYY'}
    )

    class Meta:
        model = Menu
        exclude = ('created_date',)


class ItemForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects,
        error_messages={'required': 'Please select at least one ingredient'},
        widget=forms.SelectMultiple(attrs={'class': 'width-100'})
    )

    class Meta:
        model = Item
        exclude = ('created_date',)