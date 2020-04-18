# -*- coding: utf-8 -*-

# @File: urls
# @Author : "Sampson"
# @Detail :

from django.conf.urls import url

from backend import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^add_article/$', views.add_article),
    url(r'^upload_img/$', views.upload_img)
]