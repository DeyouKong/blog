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
import logging

logger = logging.getLogger(__name__)
collect_logger = logging.getLogger('collect')


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


def register(request):
    """
    注册函数，使用forms的RegForm
    :param request:
    :return:
    """
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.cleaned_data.pop("re_password")
            avatar_img = request.FILES.get("avatar")

            # **kwarg 将字典解开成一个个类似 avatar=avatar_img的形式
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret["msg"] = "/blog/"
            collect_logger.info(form_obj.cleaned_data.get('user').username + "注册")
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            return JsonResponse(ret)

    # 生成一个 Form 对象
    form_obj = forms.RegForm()
    return render(request, "blog/register.html", {"form_obj": form_obj})


def login(request):
    """
    处理登录接口，使用极验滑动验证码登陆
    :param request:
    :return:
    """

    if request.method == "POST":
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

        valid_code = request.POST.get("valid_code")
        print(valid_code)
        print("用户输入的验证码".center(120, "="))

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)

        if result:
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                ret["msg"] = "/blog/"
            else:
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)

    return render(request, "blog/login.html")



def get_valid_img(request):
    """
    获取验证码图片的视图
    :param request:
    :return:
    """
    from PIL import Image, ImageDraw, ImageFont
    import random

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

    return redirect("/blog/")


def blogIndex(request):
    """
    博客首页
    :param request:
    :return:
    """
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

    return render(request, "blog/home.html", {
        "username": username,
        "blog": blog,
        "article_list": article_list,
    })


def article_detail(request, username, pk):
    """
    文章详情
    :param username: 被访问的 blog 的用户名
    :param pk:  访问的文章的主键 id 值
    :return:
    """
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")

    blog = user.blog
    article_obj = models.Article.objects.filter(pk=pk).first()

    return render(
        request,
        "blog/article_detail.html",
        {
            "username": username,
            "article": article_obj,
            "blog": blog,
        }
    )


@login_required()
def up_down(request):
    """
    点赞、踩
    :param request:
    :return:
    """
    article_id = request.POST.get("article_id")
    is_up = json.loads(request.POST.get("is_up"))  # 得变成 boolean
    user_id = request.user.pk
    res = {"status": True}
    collect_logger.info("点赞/踩灭：文章id" + str(article_id) + "   点赞True/踩False：" + str(is_up) + "   用户id" + str(user_id))

    try:
        with transaction.atomic():
            # 生成一条点赞踩灭信息
            models.ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
            if is_up:
                models.Article.objects.filter(pk=article_id).update(up_count=F("up_count") + 1)
            else:
                models.Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)
    except Exception as e:
        res["status"] = False
        res["first_operate"] = models.ArticleUpDown.objects.filter(article_id=article_id, user_id=user_id).first().is_up
        collect_logger.info("点赞/踩灭异常：文章id:%s，点赞True/踩False：%s，用户id：%s，异常信息：%s" %(str(article_id), str(is_up), str(user_id), e))
    return JsonResponse(res)


def comment(request):
    """
    评论，如果pid存在，则创建子评论，pid不存在，创建根评论
    :param request:
    :return:
    """
    article_id = request.POST.get('article_id')
    content = request.POST.get('content')
    pid = request.POST.get('pid')
    user_id = request.user.pk
    collect_logger.info(
        "评论：文章id：%s，评论内容：%s，用户id：%s，父评论id：%s" % (str(article_id), content, str(user_id), str(pid)))

    res = {"status": True}

    with transaction.atomic():  # 事务 有关联
        if not pid:
            obj = models.Comment.objects.create(user_id=user_id, article_id=article_id, content=content)
        else:
            obj = models.Comment.objects.create(user_id=user_id, article_id=article_id, content=content, parent_comment_id=pid)
        models.Article.objects.filter(pk=article_id).update(comment_count=F("comment_count") + 1)

    res['create_time'] = obj.create_time.strftime('%Y-%m-%d %H:%M')
    res['content'] = obj.content
    res['username'] = request.user.username
    res['pk'] = obj.pk
    if obj.parent_comment_id:
        res['pid'] = obj.parent_comment_id
        res['pidname'] = obj.parent_comment.user.username
    return JsonResponse(res)


def get_comment_tree(request,article_id):
    """
    获取评论树
    :param request:
    :param article_id: 文章id
    :return:
    """
    ret = list(models.Comment.objects.filter(article_id=article_id).values('pk','content','parent_comment_id','user__username',"create_time"))
    return JsonResponse(ret,safe=False)


import requests
def weather(request):
    """
    查看天气
    :param request:
    :return:
    """
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
