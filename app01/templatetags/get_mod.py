# -*- coding: UTF-8 -*-
# @Time : 2021-04-08 13:36
# @File : get_mod.py
# @Sofrware : PyCharm
# @Author : Du Fangyuan
from django import template

register = template.Library()
"""
自定义过滤器，在html中取余
"""
@register.filter
def get_mod(v1,v2):
    return v1 % v2