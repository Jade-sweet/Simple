# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# house_id, city,quyu,jiedao,community_name, price, longitude, latitude, area, orientation,check_in_time,floor,lift,car_station,water,power, gas, lease_term,rent_share, house_style,supporting_facilities,metro,detail_link,user_id


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    house_id = scrapy.Field()
    county = scrapy.Field()
    street = scrapy.Field()
    xiaoqu = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    detail_link = scrapy.Field()
