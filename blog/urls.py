from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r"^$", views.blogIndex),
    url(r"^comment/", views.comment),
    url(r"^up_down/(?P<pk>\d+)/$", views.up_down),
    url(r"^up_down/$", views.up_down),
    url(r"^getCommentTree/(\d+)/$", views.get_comment_tree),
    url(r"^(\w+)/article/(\d+)/$", views.article_detail),
    url(r'(?P<username>\w+)/(?P<condition>tag|cate|archive)/(?P<param>.*)', views.home),
    url(r"^(\w+)/$", views.home),

]
