"""sd_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from app01 import views
from sd_pro import settings
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),  #后台管理
    path('login/', views.login),  # 解析登录界面
    path('get_validCode_img/', views.get_validCode_img),  # 获得验证码
    path('index/', views.index), #系统首页
    re_path("^$",views.index),  #正则匹配输入网址可以不包括index字段就可以打开系统首页
    path('logout/', views.logout),  #登录后注销
    path('register/', views.register),  #新用户注册
    path('search/',views.search),  #车辆搜索
    path('type_car/',views.type_car),  #车辆类型展示
    path("digg/",views.digg),  #点赞
    path("delelove/",views.delelove),  #删除点赞
    path("comment/",views.comment),  #评论
    path("get_comment_tree/",views.get_comment_tree),  #获取评论树
    path("get_city/",views.get_city), #获取TOP10展厅
    path("show_car/",views.show_car), #智能展厅
    path("change_password/",views.change_password), #修改密码
    #  media配置
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}), #注册时头像展示

    re_path(r'^favicon\.ico$',RedirectView.as_view(url=r'static/carhome/img/web.ico'))  #网页图标静态文件
]
