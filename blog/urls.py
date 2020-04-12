from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r"^$",views.blogIndex),
    url(r"^(\w+)/article/(\d+)/$",views.article_detail),  # 文章详情
    url(r"^up_down/$",views.up_down),  # 文章详情
    url(r"^(\w+)/$",views.home),

]