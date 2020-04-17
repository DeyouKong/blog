from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from blog import forms, models
from django.contrib import auth
from django.http import JsonResponse
from geetest import GeetestLib
from django.db.models import Count, F
import json
from django.db import transaction


# Create your views here.

# 不校验 csrf
@csrf_exempt
def qigeming(request):
    if request.method == "POST":
        file_obj = request.FILES.get("file")
        print(file_obj, type(file_obj))
        with open(file_obj.name, "wb") as f:
            for line in file_obj:
                f.write(line)

    return render(request, "blog/qigeming.html")


# 注册的试图函数
def register(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        # 帮我做校验
        if form_obj.is_valid():
            # 校验通过，移除确认密码，去数据库创建一个新的用户，获取头像文件
            form_obj.cleaned_data.pop("re_password")
            avatar_img = request.FILES.get("avatar")

            # **kwarg 将字典解开成一个个类似 avatar=avatar_img的形式
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)

            # 登陆成功后，将跳转至 index页面
            ret["msg"] = "/"
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            # 有错误，就将错误信息封装到 ret["msg"] 中
            ret["msg"] = form_obj.errors
            return JsonResponse(ret)

    # 生成一个 Form 对象
    form_obj = forms.RegForm()
    return render(request, "blog/register.html", {"form_obj": form_obj})


# 使用极验滑动验证码的登陆

def login(request):
    # if request.is_ajax():  # 如果是 AJAX请求
    if request.method == "POST":
        # 初始化一个给 AJAX 返回的数据：
        ret = {"statys": 0, "msg": ""}

        username = request.POST.get("username")
        password = request.POST.get("password")

        # 获取极验  极验验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        valid_code = request.POST.get("valid_code")  # 获取用户填写的验证码
        print(valid_code)
        print("用户输入的验证码".center(120, "="))

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)

        # if valid_code and valid_code.upper() == request.session.get("valid_code","").upper():
        if result:
            # 验证码信息正确
            # 利用 auth模块 进行用户名及密码的校验
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)  # 将登陆的用户赋值给request.user
                ret["msg"] = "/"
            else:
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误"

        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)

    return render(request, "blog/login.html")


# 获取验证码图片的视图
def get_valid_img(request):
    # with open("valid_code.png", "rb") as f:
    #     data = f.read()
    # 自己生成一个图片
    from PIL import Image, ImageDraw, ImageFont
    import random

    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (220, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((20 + 40 * i, 0), tmp, fill=get_random_color(), font=font_obj)

    print("".join(tmp_list))
    print("生成的验证码".center(120, "="))
    # 不能保存到全局变量
    # global VALID_CODE
    # VALID_CODE = "".join(tmp_list)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    # 加干扰线
    # width = 220  # 图片宽度（防止越界）
    # height = 35
    # for i in range(5):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw_obj.line((x1, y1, x2, y2), fill=get_random_color())

    # 加干扰点
    # for i in range(40):
    #     draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())
    #
    #
    # 将生成的图片保存在磁盘上
    # with open("s10.png", "wb") as f:
    #     img_obj.save(f, "png")
    # # 把刚才生成的图片返回给页面
    # with open("s10.png", "rb") as f:
    #     data = f.read()

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    from io import BytesIO
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)


# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "505fcf7f678fba6923e365ac66ca35a6"
pc_geetest_key = "2ea9ec97a8eb08fdb2ec1041d34456ba"


# 处理极验 获取验证码的视图
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 注销
def logout(request):
    auth.logout(request)

    return redirect("/")


def blogIndex(request):
    # 查询所有的文章列表
    article_list = models.Article.objects.all()

    return render(request, "blog/blog_index.html", {"article_list": article_list})


def index(request):
    return render(request, "index.html")


def home(request, username):
    """
    个人博客主页
    :param request:
    :param username: 倍访问博客对象用户名称
    :return:
    """
    user = models.UserInfo.objects.filter(username=username).first()

    if not user:
        return HttpResponse("404")

    blog = user.blog
    article_list = models.Article.objects.filter(user=user)

    """
    # 我的文章分类及每个分类下的文章数
    # 将我的文章按照我的分类分组，并统计出每个分类下的文章数


    # 查询某个分类对应的文章
    user = models.UserInfo.objects.filter(username="xiaohei").first()  # 拿到 xiaohei 的用户对象
    blog = user.blog   # 得到 xiaohei 用户对应的 blog 站点对象
    ret = models.Category.objects.filter(blog=blog)  # 求 xiaohei 站点下的文章分类信息

    # ret = ret[0].article_set.all()  # 查询 ret[0] 分类下面的所有文章

    for i in ret:
 

    # category_list = models.Category.objects.filter(blog=blog)

    # 查询某个分类对应的文章
    # category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title","c")

    # 统计当前站点下有哪些标签，并且按标签统计出文章数
    # tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title","c")

    # 按照 日期 归档
    # models.Article.objects.filter(user=user).values("create_time").annotate(time=Count("article"))

    # 执行一条 sql 语句
    # ret = models.Article.objects.filter(user=user).extra(
    #     select={"c":"date_format(create_time,'%Y-%m')"}
    # )

    # archive_list = models.Article.objects.filter(user=user).extra(
    #     select={"archive_ym":"Strftime(create_time,'%%Y-%%m')"}
    # ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym","c")

    # category_list, tag_list, archive_list = get_left_menu(username)
    
           print(i.title,i.article_set.all().count())
    """

    # print("这里是home页面")

    return render(request, "blog/home.html", {
        "username": username,
        "blog": blog,
        "article_list": article_list,
    })


def article_detail(request, username, pk):
    """
    :param username: 被访问的 blog 的用户名
    :param pk:  访问的文章的主键 id 值
    :return:
    """

    # 获取被访问的用户名是否存在
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")

    blog = user.blog

    # # 查询某个分类对应的文章
    # category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    #
    # # 统计当前站点下有哪些标签，并且按标签统计出文章数
    # tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    #
    # # 按照 日期 归档
    # archive_list = models.Article.objects.filter(user=user).extra(
    #     select={"archive_ym": "Strftime(create_time,'%%Y-%%m')"}
    # ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")

    # 获取文章的详情信息
    article_obj = models.Article.objects.filter(pk=pk).first()

    # category_list, tag_list, archive_list = get_left_menu(username)

    return render(
        request,
        "blog/article_detail.html",
        {
            "username": username,
            "article": article_obj,
            "blog": blog,
        }
    )


# 处理点赞踩灭
@login_required()
def up_down(request):
    article_id = request.POST.get("article_id")
    is_up = json.loads(request.POST.get("is_up"))  # 得变成 boolean
    user_id = request.user.pk
    res = {"status": True}
    print(article_id, is_up, user_id)

    try:
        with transaction.atomic():
            # 生成一条点赞踩灭信息
            models.ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
            if is_up:
                models.Article.objects.filter(pk=article_id).update(up_count=F("ip_count") + 1)
            else:
                models.Article.objects.filter(pk=article_id).update(down_count=F("down_count") - 1)
    except Exception as e:
        res["status"] = False
        res["first_operate"] = models.ArticleUpDown.objects.filter(article_id=article_id, user_id=user_id).first()
    print(res)
    return JsonResponse(res)


# 评论
def comment(request):
    article_id = request.POST.get('article_id')
    content = request.POST.get('content')
    pid = request.POST.get('pid')
    user_id = request.user.pk

    res = {"state": True}

    with transaction.atomic():  # 事务 有关联
        if not pid:  # 提交根评论
            obj = models.Comment.objects.create(user_id=user_id, article_id=article_id, content=content)
        else:  # 提交子评论
            obj = models.Comment.objects.create(user_id=user_id, article_id=article_id, content=content, parent_comment_id=pid)

        # comment_count 加 + 1
        models.Article.objects.filter(pk=article_id).update(comment_count=F("comment_count") + 1)

    res['time'] = obj.create_time.strftime('%Y-%m-%d %H:%M')
    res['content'] = obj.content
    if obj.parent_comment_id:
        res['pid'] = obj.parent_comment_id
        res['pidname'] = obj.parent_comment.user.username
    return JsonResponse(res)


# 获取评评论树
def get_comment_tree(request,article_id):
    ret = list(models.Comment.objects.filter(article_id=article_id).values('pk','content','parent_comment_id','user__username',"create_time"))
    print(ret)
    return JsonResponse(ret,safe=False)


# 处理查看天气
import requests
def weather(request):
    ip_api = "https://api.map.baidu.com/location/ip?ak=wwEmIVc2ZVFcsFQdMW2MMsmGln0uRLxU"
    response = requests.get(ip_api)
    city_dict = response.json()
    nowcity = city_dict["content"]["address_detail"]["city"]
    if request.method == "POST":
        city = request.POST["city"]
        str = "http://api.map.baidu.com/weather/v1/?district_id=222405&data_type=all&ak=wwEmIVc2ZVFcsFQdMW2MMsmGln0uRLxU&output=json"
    else:
        str = "http://api.map.baidu.com/weather/v1/?district_id=222405&data_type=all&ak=wwEmIVc2ZVFcsFQdMW2MMsmGln0uRLxU&output=json"

    response = requests.get(str)
    json_str = response.text
    json_dict = json.loads(json_str)
    data_dict = json_dict['result']
    print(data_dict)
    now = data_dict["now"]
    # index = lin['now']
    w_date = data_dict['forecasts']

    city = data_dict["location"]['city']
    # pm = data_dict[0]['pm25']
    # print('城市：{}; pm25：{};'.format(city, pm))

    nowtq = w_date[0]
    onetq = w_date[1]
    twotq = w_date[2]
    threetq = w_date[3]
    fourtq = w_date[4]
    for item_dict1 in w_date:
        date = item_dict1['date']
        temperature = item_dict1['high']
        weather = item_dict1['text_day']
        wind = item_dict1['wd_night']
        print('时间：{}; 温度：{}; 天气：{}; 风向：{}'.format(date, temperature, weather, wind))
    context = {
        'city': city,
        'weather_list': w_date,
        'nowtq': nowtq,
        'onetq': onetq,
        'twotq': twotq,
        'threetq': threetq,
        'fourtq': fourtq,
        'nowcity': nowcity,
    }
    return render(request, template_name='weather.html', context=context)


def test(request):
    return render(request, "test.html")


def forMyLover(request):
    return render(request, "myIndex.html")
