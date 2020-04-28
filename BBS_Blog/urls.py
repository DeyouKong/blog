"""BBS_Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from blog import views
from testcase import urls as  testcase_urls
from django.conf import settings
from django.views.static import serve
from blog import urls as blog_urls
from backend import urls as backend_urls

urlpatterns = [

    url(r"^$",views.index),
    url(r"^index/$",views.index),
    url(r"^register/",views.register),
    url(r"^login/",views.login),
    url(r"^logout/",views.logout),


    url(r'^get_valid_img.png/', views.get_valid_img),
    # 极验滑动验证码 获取验证码的url
    url(r'^pc-geetest/register', views.get_geetest),
    # 上传文件操作
    url(r"^qigeming/$",views.qigeming),
    # 查看天气
    url(r"^weather/$",views.weather),
    url(r"^forMyLover/$", views.forMyLover),
    url(r"^specialPhoto/$", views.specialPhoto),

    url(r"^media/(?P<path>.*)$",serve,{"document_root":settings.MEDIA_ROOT}),
    # 将所有以 blog开头的url 都交给 app 下面的 urls.py 来处理
    url(r"^blog/",include(blog_urls)),
    url(r"^testcase/", include(testcase_urls)),
    url(r'^backend/', include(backend_urls)),
    url('admin/', admin.site.urls),
    url(r"test/$", views.test),


]
