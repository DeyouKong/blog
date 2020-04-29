# -*- coding: utf-8 -*-

# @File: functions
# @Author : "Sampson"
# @Detail :


from django.conf.urls import url
from testcase import views

urlpatterns = [
    url(r"delRedis/$",views.delRedis),
    url(r"$",views.index),


    # url(r"^(\w+)/article/(\d+)/$",views.article_detail),  # 文章详情

]

