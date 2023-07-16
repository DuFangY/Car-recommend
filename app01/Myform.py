# -*- coding: UTF-8 -*-
# @Time : 2021-03-14 22:01
# @File : Myform.py
# @Sofrware : PyCharm
# @Author : Du Fangyuan
from django import forms
from django.forms import widgets
from app01.models import UserInfo
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


class UserForm(forms.Form):
    user = forms.CharField(max_length=32,
                           error_messages={"required": "该字段不能为空"},
                           label="用户名",
                           widget=widgets.TextInput(attrs={"class": "form-control"}
                                                    )
                           )

    pwd = forms.CharField(max_length=32,
                          error_messages={"required": "该字段不能为空"},
                          label="密码",
                          widget=widgets.PasswordInput(attrs={"class": "form-control"}
                                                       )
                          )
    re_pwd = forms.CharField(max_length=32,
                             error_messages={"required": "该字段不能为空"},
                             label="确认密码",
                             widget=widgets.PasswordInput(attrs={"class": "form-control"}
                                                          )
                             )
    telephone = forms.CharField(max_length=32,
                                error_messages={"required": "该字段不能为空"},
                                label="电话号码",
                                widget=widgets.TextInput(attrs={"class": "form-control"}
                                                         )
                                )

    #############################局部钩子和全局钩子校验##############################
    def clean_user(self):
        val = self.cleaned_data.get("user")

        user = UserInfo.objects.filter(username=val).first()
        if not user:  # 未被注册
            return val
        else:  # 用户已被注册
            raise ValidationError("该用户已注册！")

    def clean(self):
        pwd_ = self.cleaned_data.get("pwd")
        re_pwd_ = self.cleaned_data.get("re_pwd")
        if pwd_ and re_pwd_:
            if pwd_ == re_pwd_:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data

    def clean_telephone(self):
        telephone_ = self.cleaned_data.get("telephone")
        telephone = UserInfo.objects.filter(telephone=telephone_).first()
        if not telephone:  # 未被注册
            return telephone_
        else:  # 用户已被注册
            raise ValidationError("该手机号已被注册！")
