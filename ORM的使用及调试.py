import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE","BBS_Blog.settings")
    import django
    django.setup()

    from blog import models


# ------ 基于 对象 的查询 SQL: 子查询
#     a1 = models.Article.objects.first()
#     print(a1.user.avatar, type(a1.user))

# ------ 基于 QuerySet 查询, SQL: join连表查询
#     a2 = models.Article.objects.filter(pk=2)
#     print(a2.values("user__avatar"))


# 查询a1对应的评论数
#     ret = models.Article.objects.first().comment_set.all()
#     print(ret)

 # 查询某个分类对应的文章
    from django.db.models import Count

    user = models.UserInfo.objects.filter(username="xiaohei").first()
    blog = user.blog

    # ret = models.Category.objects.filter(blog=blog)  # 求小黑站点下面所有的文章分类
    # ret = ret[0].article_set.all()  # 技术分类下面所有的文章
    # for i in ret:
    #     print(i.title, i.article_set.all().count())


# ret = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    # print(ret)
    # 基于QuerySet查询的时候 不用加set
    # models.Category.objects.filter(blog=blog).values("article__title")


    # ret = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    # print(ret)

# 基于QuerySet查询的时候 不用加set
    # models.Category.objects.filter(blog=blog).values("article__title")

    # 基于时间归档
    # ret = models.Article.objects.filter(user=user).extra(
    #     select={"archive_ym":"date(create_time,'%%Y-%%m')"}
    # ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym","c")
    #
    # print(ret)

    article_obj = models.Article.objects.filter(pk=1).first()
    print(article_obj,type(article_obj))
    print("="*120)
    ret = models.Article.objects.filter(pk=1).values("articledetail__content")
    print(ret)