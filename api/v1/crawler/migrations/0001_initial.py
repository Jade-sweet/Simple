# Generated by Django 2.1.13 on 2020-12-13 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HouseInfo',
            fields=[
                ('house_id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='唯一编号')),
                ('county', models.CharField(max_length=32, verbose_name='区')),
                ('street', models.CharField(max_length=32, verbose_name='街道')),
                ('xiaoqu', models.CharField(max_length=32, verbose_name='小区名')),
                ('price', models.IntegerField(default=0, verbose_name='价格')),
                ('area', models.IntegerField(default=0, verbose_name='面积')),
                ('detail_link', models.CharField(max_length=128, verbose_name='详情链接')),
            ],
            options={
                'db_table': 'houseInfo',
            },
        ),
    ]
