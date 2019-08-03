from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^menu/item/(?P<pk>\d+)/edit/$', views.item_edit, name='item_edit'),
    url(r'^menu/item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.edit_menu, name='menu_edit'),
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='menu_detail'),
    url(r'^menu/item/$', views.item_list, name='item_list'),
    url(r'^menu/new/$', views.create_new_menu, name='menu_new'),
    url(r'^$', views.home, name='home')
]