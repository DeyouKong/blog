from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11,null=True,unique=True,verbose_name="手机号")  # 文章标题，verbose_name 设置在admin中的别名)
    # upload_to 前段传送过来的文件都保存在这个文件夹，如果不存在，自动创建
    avatar = models.FileField(upload_to="avatars/",default="avatars/default.png")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    blog = models.OneToOneField(to="Blog",to_field="nid",null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        # 设置在 admin 后台管理中，表的别名
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        # 如果无此设置，当数量为多个时，显示为 "用户s"


class Blog(models.Model):
    """
    博客信息表
    """
    nid = models.AutoField(primary_key=True)
    title =models.CharField(max_length=64)  # 个人博客标题
    site = models.CharField(max_length=32,unique=True) # 个人博客后缀
    theme = models.CharField(max_length=32)   # 博客主题
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")


    def __str__(self):
        return self.title

    class Meta:
        # 设置在 admin 后台管理中，表的别名
        verbose_name = "blog站点"
        verbose_name_plural = verbose_name
        # 如果无此设置，当数量为多个时，显示为 "用户s"



class Category(models.Model):
    """
    个人博客文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)   # 分类标题
    blog = models.ForeignKey(to="Blog",to_field="nid",on_delete=models.DO_NOTHING)  # 外键关联博客，一个博客站点可以有多个分类
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        # 设置在 admin 后台管理中，表的别名
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name
        # 如果无此设置，当数量为多个时，显示为 "用户s"



class Tag(models.Model):
    """
    标签
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)   # 标签名
    blog = models.ForeignKey(to="Blog",to_field="nid",on_delete=models.DO_NOTHING)   # 所属博客
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        # 设置在 admin 后台管理中，表的别名
        verbose_name = "标签"
        verbose_name_plural = verbose_name
        # 如果无此设置，当数量为多个时，显示为 "用户s"



class Article(models.Model):
    """
    文章
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50,verbose_name="文章标题")  # 文章标题，verbose_name 设置在admin中的别名
    desc = models.CharField(max_length=255,verbose_name="文章描述")  # 文章描述
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间

    category = models.ForeignKey(to="Category", to_field="nid", null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(to="UserInfo", to_field="nid",on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(  # 中介模型
        to="Tag",
        through="Article2Tag",
        through_fields=("article", "tag"),  # 注意顺序！！！
    )
    comment_count = models.IntegerField(verbose_name="评论数",default=0)
    up_count = models.IntegerField(verbose_name="点赞数",default=0)
    down_count = models.IntegerField(verbose_name="踩数",default=0)

    def __str__(self):
        return self.title

    class Meta:
        # 设置在 admin 后台管理中，表的别名
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        # 如果无此设置，当数量为多个时，显示为 "用户s"



class ArticleDetail(models.Model):
    """
    文章详情表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to="Article", to_field="nid",on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    class Meta:
        # 设置在 admin 后台管理中，表的别名
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name
        # 如果无此设置，当数量为多个时，显示为 "用户s"
        # unique_together = ("article")


class Article2Tag(models.Model):
    """
    文章和标签的多对多关系表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid",on_delete=models.CASCADE)
    tag = models.ForeignKey(to="Tag", to_field="nid",on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    def __str__(self):
        return "{}-{}".format(self.article.title,self.tag.title)

    class Meta:
        unique_together = (("article", "tag"),)
        # 设置在 admin 后台管理中，表的别名
        verbose_name = "文章-标签"
        verbose_name_plural = verbose_name
        # 如果无此设置，当数量为多个时，显示为 "用户s"



class ArticleUpDown(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", null=True,on_delete=models.DO_NOTHING)
    article = models.ForeignKey(to="Article", null=True,on_delete=models.DO_NOTHING)
    is_up = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    class Meta:
        unique_together = (("article", "user"),)

        # 设置在 admin 后台管理中，表的别名
        verbose_name = "文章点赞"
        verbose_name_plural = verbose_name
        # 如果无此设置，当数量为多个时，显示为 "用户s"


class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid",on_delete=models.DO_NOTHING)
    user = models.ForeignKey(to="UserInfo", to_field="nid",on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=255)  # 评论内容
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self", null=True,on_delete=models.DO_NOTHING,blank=True)  # 在Django admin 里面也可以不填

    def __str__(self):
        return self.content

    class Meta:
        # 设置在 admin 后台管理中，表的别名
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        # 如果无此设置，当数量为多个时，显示为 "用户s"


