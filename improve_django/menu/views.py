from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from operator import attrgetter
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *


def home(request):
    all_menus = Menu.objects.order_by('expiration_date')
    menus = []

    for menu in all_menus:
        if (
            (menu.expiration_date is not None) and
            (menu.expiration_date < timezone.now())
        ):
            continue
        menus.append(menu)

    return render(request, 'menu/home.html', {'menus': menus})


def menu_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/item_detail.html', {'item': item})

def item_list(request):
    items = Item.objects.order_by('name')
    return render(request, 'menu/item_list.html', {'items': items})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)

        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            form.save_m2m() # required when using commit=False

            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_create.html', {'form': form})

def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)

    form = MenuForm(instance=menu)

    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'menu/menu_edit.html', {
        'form': form
        })