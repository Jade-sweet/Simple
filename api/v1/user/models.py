from datetime import datetime

from django.db import models

# Create your models here.


class User(models.Model):
    """用户表"""
    name = models.CharField(max_length=128, null=False, unique=True)
    nick_name = models.CharField(max_length=128)
    password = models.CharField(max_length=64)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        db_table = 'user'


class Token(models.Model):
    """用于记录token"""
    tid = models.CharField(max_length=128, primary_key=True)
    uid = models.IntegerField()
    expire_time = models.DateTimeField(default=datetime(1999, 1, 1, 0, 0, 0))  # 自动过期时间
    is_expire = models.BooleanField(default=False)  # 手动过期时使用
    objects = models.Manager()

    class Meta:
        db_table = 'token'
