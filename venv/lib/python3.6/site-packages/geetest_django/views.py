# coding: utf-8
import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from geetest import GeetestLib

from geetest_django.forms import GeeForm
from geetest_django.utils import load_resp, set_geetest_passed


captcha_id = getattr(settings, "GEETEST_ID")
private_key = getattr(settings, "GEETEST_KEY")


GEETEST_UID_NAME = "geetest_uid"


def _get_or_create_session_key(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    return request.session.session_key


def gee_captcha_view(request):
    if request.method == 'GET':
        return _get_captcha(request)
    if request.method == 'POST':
        return _ajax_validate_captcha(request)
    return HttpResponseNotAllowed("error")


def _get_captcha(request):
    session_id = _get_or_create_session_key(request)
    gt = GeetestLib(captcha_id, private_key)
    status = gt.pre_process(session_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session[GEETEST_UID_NAME] = session_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def _ajax_validate_captcha(request):
    gt = GeetestLib(captcha_id, private_key)
    form = load_resp(request.body, GeeForm)
    if form is None:
        return HttpResponseBadRequest(
            json.dumps({"message": "Bad request"})
        )
    if not form.is_valid():
        return HttpResponseBadRequest(
            json.dumps(
                {"message": form.errors.as_json()}
            )
        )
    status = request.session[gt.GT_STATUS_SESSION_KEY]
    user_id = request.session[GEETEST_UID_NAME]
    challenge = form.cleaned_data[gt.FN_CHALLENGE]
    validate = form.cleaned_data[gt.FN_VALIDATE]
    seccode = form.cleaned_data[gt.FN_SECCODE]
    if status:
        result = gt.success_validate(
            challenge, validate, seccode, user_id
        )
    else:
        result = gt.failback_validate(challenge, validate, seccode)
    if result:
        set_geetest_passed(request)
        return HttpResponse(json.dumps({"message": "成功"}))
    return HttpResponseBadRequest(json.dumps({"message": "验证码错误"}))
