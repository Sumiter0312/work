from django.db import models

class User(models.Model):
    username = models.CharField(max_length=15,unique=True)
    password = models.CharField(max_length=15)

class Data(models.Model):
    str = models.CharField(verbose_name="随机字符串",max_length=50)
    len = models.PositiveIntegerField(verbose_name='字符串长度')
