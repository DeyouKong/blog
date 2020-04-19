from django import template
from blog import models
from django.db.models import Count

register = template.Library()


@register.inclusion_tag("blog/left_menu.html")
def get_left_menu(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog


    # 查询某个分类对应的文章
    category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")

    # 统计当前站点下有哪些标签，并且按标签统计出文章数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")

    # 按照 日期 归档
    archive_list = models.Article.objects.filter(user=user).extra(
        select={"archive_ym": "Strftime(create_time,'%%Y-%%m')"}
    ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")

    # 应当返回一个字典形式
    return {
        "user": user,
        "category_list":category_list,
        "tag_list":tag_list,
        "archive_list":archive_list
    }
