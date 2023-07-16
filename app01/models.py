# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    avatar = models.FileField(upload_to='avatars/', default='/avatars/default.png')

    def __str__(self):
        return self.username


class CarType(models.Model):
    """
    车辆类型表
    """
    nid = models.AutoField(primary_key=True)
    type_car = models.CharField(max_length=11, unique=True)
    url = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.url


class Car(models.Model):
    """
    具体车辆信息表
    """
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True,null=True)
    type = models.CharField(max_length=11)
    car_url = models.CharField(max_length=255, unique=True,null=True)
    img_url = models.CharField(max_length=255, null=True)
    price = models.CharField(max_length=64,null=True)
    score = models.DecimalField(max_digits=3,decimal_places=2,null=True)
    sales_inf = models.CharField(max_length=20,null=True)
    brand = models.CharField(max_length=40,null=True)

    comment_count = models.IntegerField(default=0)   #评论个数
    up_count = models.IntegerField(default=0)    #车辆点赞喜欢个数
    down_count = models.IntegerField(default=0)    #车辆不喜欢个数
    hot_score = models.FloatField(default=-99999)  #热度评分
    def __str__(self):
        return self.name

class car_love(models.Model):
    """
    车辆喜欢列表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True, on_delete=models.CASCADE)
    car = models.ForeignKey('Car', null=True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)   #是否喜欢
    class Meta:
        unique_together = [
            ('car', 'user'),
        ]

class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='评论者',to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    car = models.ForeignKey(verbose_name='评论车辆',to='Car',to_field='nid',on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    content = models.CharField(verbose_name='评论内容',max_length=255)

    parent_comment = models.ForeignKey('self',null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.content


