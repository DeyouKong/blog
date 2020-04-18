from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r"^$",views.blogIndex),
    url(r"^(\w+)/article/(\d+)/$",views.article_detail),
    url(r"^up_down/$",views.up_down),
    url(r"^(\w+)/$",views.home),
    url(r"^comment/", views.comment),
    url(r"^getCommentTree/(\d+)/$", views.get_comment_tree),

]