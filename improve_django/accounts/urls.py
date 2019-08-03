from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'login/$', views.login, name='login'),
    url(r'sign_up/$', views.sign_up, name='sign_up'),
    url(r'logout/$', views.logout, name='logout'),
]