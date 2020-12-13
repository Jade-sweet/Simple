from django.db import models

# Create your models here.


class HouseInfo(models.Model):
    house_id = models.CharField(primary_key=True, max_length=50, verbose_name='唯一编号')
    county = models.CharField(max_length=32, verbose_name='区')
    street = models.CharField(max_length=32, verbose_name='街道')
    xiaoqu = models.CharField(max_length=32, verbose_name='小区名')
    price = models.IntegerField(default=0, verbose_name='价格')
    area = models.IntegerField(default=0, verbose_name='面积')
    detail_link = models.CharField(max_length=128, verbose_name='详情链接')
    objects = models.Manager()

    class Meta:
        db_table = 'houseInfo'
