# coding=utf-8

from django.conf.urls import url

from post import views


urlpatterns = [
    url(r'^index/$', views.post_index_page, name='index'),
]
