from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

from testcase import common

def index(request):
    return render(request, "TestPlatform/index.html")


def delUser(request):
    userId = request.POST.get("userID", None)

def delRedis(request):
    env = request.POST.get("env", None)
    db = request.POST.get("db", 0)
    channel = request.POST.get("channel", "W")
    open_id = request.POST.get("openID", None)
    union_id = request.POST.get("unionID", None)
    user_id = request.POST.get("userID", None)

    ret = {"code": "0", "msg": "success"}
    print(env,db,channel,open_id,union_id,user_id)

    if env in ["test", "new-vip", "go-test-5", "staging", "staging2"]:
        if channel in ["W", "Z"]:
            r = common.connectRedis(env, db=db)
            delRet = common.delRedis(r, channel, open_id, union_id, user_id)
        else:
            ret["code"] = 1
            ret["msg"] = "渠道输入有误，请检查"
    else:
        ret["code"] = 1
        ret["msg"] = "测试环境输入有误，请检查"

    print(ret)

    return JsonResponse(ret)




