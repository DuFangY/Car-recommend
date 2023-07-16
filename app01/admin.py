from django.contrib import admin

# Register your models here.
from app01 import models
admin.site.register(models.UserInfo)
# admin.site.register(models.Personwebsite)
admin.site.register(models.CarType)
admin.site.register(models.Car)
admin.site.register(models.car_love)
admin.site.register(models.Comment)