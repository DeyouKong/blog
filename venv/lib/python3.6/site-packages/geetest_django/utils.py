import json

from django.http import JsonResponse

_GEETEST_PASSED_KEY = "geetest_passed"


def resp(data=None, description="", code=0):
    return JsonResponse(
        {
            "errorCode": code,
            "description": description,
            "data": data,
        },
    )


def load_resp(raw_data, form_cls):
    data = load_data(raw_data)
    if data is None:
        return
    return form_cls(data)


def set_geetest_passed(request):
    request.session[_GEETEST_PASSED_KEY] = True


def is_geetest_passed(reqeust):
    return reqeust.session.get(_GEETEST_PASSED_KEY)


def load_data(raw_data):
    try:
        return json.loads(raw_data)
    except ValueError:
        return None