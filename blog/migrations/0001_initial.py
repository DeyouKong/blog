# Generated by Django 2.1.7 on 2020-04-19 02:53

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=11, null=True, unique=True, verbose_name='手机号')),
                ('avatar', models.FileField(default='avatars/default.png', upload_to='avatars/')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, verbose_name='文章标题')),
                ('desc', models.CharField(max_length=255, verbose_name='文章描述')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('comment_count', models.IntegerField(default=0, verbose_name='评论数')),
                ('up_count', models.IntegerField(default=0, verbose_name='点赞数')),
                ('down_count', models.IntegerField(default=0, verbose_name='踩数')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Article2Tag',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article')),
            ],
            options={
                'verbose_name': '文章-标签',
                'verbose_name_plural': '文章-标签',
            },
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.Article')),
            ],
            options={
                'verbose_name': '文章详情',
                'verbose_name_plural': '文章详情',
            },
        ),
        migrations.CreateModel(
            name='ArticleUpDown',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('is_up', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '文章点赞',
                'verbose_name_plural': '文章点赞',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('site', models.CharField(max_length=32, unique=True)),
                ('theme', models.CharField(max_length=32)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'blog站点',
                'verbose_name_plural': 'blog站点',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Blog')),
            ],
            options={
                'verbose_name': '文章分类',
                'verbose_name_plural': '文章分类',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=255)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Article')),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Blog')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(through='blog.Article2Tag', to='blog.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='blog',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Blog'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='articleupdown',
            unique_together={('article', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together={('article', 'tag')},
        ),
    ]
