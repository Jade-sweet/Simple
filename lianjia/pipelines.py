# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymysql
import sqlite3
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from lianjia.items import LianjiaItem


class LianjiaMysqlPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, LianjiaItem):
            print(item['house_id'], item['county'], item['street'], item['xiaoqu'], item['price'], item['area'], item['detail_link'])
            sql = 'insert into houseInfo(house_id, county, street, xiaoqu, price, area, detail_link) values (?, ?, ?, ?, ?, ?, ?)'
            try:
                self.cursor.execute(sql, (item['house_id'], item['county'], item['street'], item['xiaoqu'], item['price'], item['area'], item['detail_link']))
            except Exception as e:
                sql2 = "update houseInfo set price=? where house_num=?"
                self.cursor.execute(sql2, (item['price'], item['house_id']))
        else:
            pass
        self.db.commit()
        return item

    def __init__(self, host, username, password, port, database):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings.get('MYSQL_HOST'), username=crawler.settings.get('MYSQL_USERNAME'),
                   password=crawler.settings.get('MYSQL_PASSWORD'), database=crawler.settings.get('MYSQL_DATABASE'),
                   port=crawler.settings.get('MYSQL_PORT'))

    # 蜘蛛对象生成的时候调用
    def open_spider(self, spider):
        # self.db = pymysql.connect(self.host, self.username, self.password, self.database, charset='utf8',
        #                           port=self.port)
        # self.cursor = self.db.cursor()

        self.db = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3'))
        self.cursor = self.db.cursor()

    # 蜘蛛关闭的时候调用
    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
