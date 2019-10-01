"""
BBS用到的 form 类
"""

from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from blog import models

# 定义一个注册的 form 类

class RegForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label="用户名",
        error_messages={
            "max_length":"用户名最长16位",
            "required":"用户名不能为空",
        },
        widget=widgets.TextInput(
            attrs={"class":"form-control"},
        )
    )
    password = forms.CharField(
        min_length=6,
        max_length=16,
        label="密码",
        error_messages={
            "min_length": "密码长度最小6位",
            "max_length": "密码长度最大16位",
            "required": "密码不能为空",
        },
        widget=widgets.PasswordInput(
            attrs={"class": "form-control"},
        )
    )
    re_password = forms.CharField(
        min_length=6,
        max_length=16,
        label="确认密码",
        widget=widgets.PasswordInput(
            attrs={"class": "form-control"},
        ),
        error_messages={
            "min_length": "确认密码长度最小6位",
            "max_length": "确认密码长度最大16位",
            "required": "确认密码不能为空",
        },
    )
    email = forms.EmailField(
        label="邮箱",
        widget=widgets.EmailInput(
            attrs={"class": "form-control"},
        ),
        error_messages={
            "required": "邮箱不能为空",
            "invalid":"邮箱格式不正确",
        },
    )


    # 局部钩子只对某个字段做校验，做完校验后返回该字段，而不是全部数据

    # 重写 username 字段的局部钩子
    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            # 表示用户名已经注册
            self.add_error("username",ValidationError("用户名已存在"))
        else:
            return username

    # 重写 email 字段的局部钩子
    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_exist = models.UserInfo.objects.filter(email=email)
        if is_exist:
            # 表示邮箱已经被注册
            self.add_error("email", ValidationError("邮箱已被注册"))
        else:
            return email

    # 重写全局钩子函数，对确认密码进行校验
    # 全局钩子没有错误的话需要返回传过来的全部数据 -- cleaned_data
    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")

        if password and password != re_password:
            self.add_error("re_password",ValidationError("两次密码不一致"))

        else:
            return self.cleaned_data