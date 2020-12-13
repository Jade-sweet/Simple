# -*- coding: utf-8 -*-
import json
import re
import os
import time
from math import ceil
import jieba
import scrapy
from django.http import request
from lxml import etree
from lianjia.items import *
from lianjia.spiders.proxy_helper import *
from my_lib.code_encryption import obj_decode

DICT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://cd.lianjia.com/zufang/pg2rs%E9%BE%99%E6%B3%89%E9%A9%BF/']

    def __init__(self, house_type=None, area=None, *args, **kwargs):
        super(SpiderSpider, self).__init__(*args, **kwargs)
        self.area = json.loads(obj_decode(area).decode('utf-8'))
        # 拼接的url
        url = 'https://cd.lianjia.com/ershoufang/%s/' % self.area[1] if house_type == '二手房' else 'https://cd.fang.lianjia.com/loupan/%s/' % self.area[1]
        self.start_urls = [url]
        self.house_type = house_type

    # 取得首页
    def start_requests(self):
        headers = {
            'Host': 'cd.lianjia.com' if self.house_type == '二手房' else 'cd.fang.lianjia.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.79 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        url = self.start_urls[0]
        try:
            yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse_total, dont_filter=False,
                                 meta={'url': url})
        except Exception as e:
            time.sleep(3)
            self.proxies_ip = get_proxies()
            yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse_total, dont_filter=False,
                                 meta={'url': url})
        finally:
            print('+'*30)

    # 计算需要访问多少页
    def parse_total(self, response):
        html_data = response.text
        etree_html = etree.HTML(html_data)
        if self.house_type == '二手房':
            house_count = etree_html.xpath('//div[@class="resultDes clear"]/h2[@class="total fl"]/span/text()')
        else:
            house_count = etree_html.xpath('//div[@class="resblock-have-find"]//span[@class="value"]/text()')
        # 得到总数，从而计算页数
        count = int(house_count[0].strip(' '))
        # 每一页的最大个数
        max_num = 20 if self.house_type == '二手房' else 10
        page_count = (count // max_num) + 1
        page_count = page_count if page_count <= 100 else 101
        # for url_page in range(page_count, 1, -1):
        for url_page in range(1, 2):  # 这里控制一次爬虫的爬取数量
            headers = {
                'Host': 'cd.lianjia.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/79.0.3945.79 Safari/537.36',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cookie':'lianjia_uuid=b9682195-b603-4888-9349-e5c478c840ec; _smt_uid=5eb76f1b.3dd66059; _ga=GA1.2.371782202.1589079838; select_city=510100; UM_distinctid=1765a8d1eea308-049b130530f675-c791039-1fa400-1765a8d1eeb4a9; _jzqc=1; _jzqckmp=1; _gid=GA1.2.2138447179.1607836969; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1607837101; gr_user_id=1d280100-3aad-4fab-a9b2-ad6bea26df77; _jzqa=1.2641463273742878000.1589079836.1607836967.1607841673.3; _jzqy=1.1607841749.1607841749.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.-; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22171fc8a058d94e-054cdeb23af75b-d373666-2073600-171fc8a058e7eb%22%2C%22%24device_id%22%3A%22171fc8a058d94e-054cdeb23af75b-d373666-2073600-171fc8a058e7eb%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E9%93%BE%E5%AE%B6%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wychengdu%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1607841753; lianjia_ssid=bce1fa92-9fb9-4bf6-9f9f-c72dd3bc5091; CNZZDATA1256144579=644515530-1607849362-%7C1607849362; CNZZDATA1254525948=713186687-1607850635-%7C1607850635; CNZZDATA1255633284=110738645-1607850675-%7C1607850675; CNZZDATA1255604082=1936251869-1607850635-%7C1607850635; gr_session_id_a1a50f141657a94e=757af112-d87c-4742-88ff-d66a51ae7466; _qzjc=1; _jzqc=1; gr_session_id_a1a50f141657a94e_757af112-d87c-4742-88ff-d66a51ae7466=true; _jzqa=1.2641463273742878000.1589079836.1607836967.1607841673.3; lj_newh_session=eyJpdiI6IlhUZE11U1Rtd1NPbHpMUWtUV1wveDNnPT0iLCJ2YWx1ZSI6ImVsU0x1VmxvaG1hVW1rcmFjQnV5Qk0raUdSTDl3M1VRaGs0VGdIT1hBQVJ3U2dEUmM4bjhOSjg0N3hKRnFzajA1UzJQV0ZhSWdiOFpUS01nd0syNGF3PT0iLCJtYWMiOiJiZjIyNGQxODNlOTBkZGU5NWYyZmI0ZjY3NGQ3ZTBkYWU1N2IzMmVhYmE5N2QwNzQ1YjdjMjk3Njk5MTVjM2NiIn0%3D; _qzja=1.1250997479.1607851516207.1607851516207.1607851516207.1607851661818.1607851897040.0.0.0.3.1; _qzjb=1.1607851516207.3.0.0.0; _qzjto=3.1.0; _jzqb=1.3.10.1607851516.1; srcid=eyJ0IjoiXCJ7XFxcImRhdGFcXFwiOlxcXCI3ZTE5YWZlZGZjYjdiM2M1MDhlMWYzMDQ2YzRlY2RjNDU1ZmM5YTFkYWZlNWI3YjJhMTQ3YjZjZmQ4MTQ5NTY3M2M5NTQ0NDFkZmY5YzU3'
            }
            url = self.start_urls[0] + 'pg%d/' % url_page

            call_back_func = self.ershou_parse if self.house_type == '二手房' else self.new_house_parse

            try:
                yield scrapy.Request(url=url, headers=headers, method='GET', callback=call_back_func, dont_filter=False,
                                     meta={'url': url})
            except:
                time.sleep(3)
                self.proxies_ip = get_proxies()
                yield scrapy.Request(url=url, headers=headers, method='GET', callback=call_back_func, dont_filter=False,
                                     meta={'url': url})
            finally:
                print('+' * 30)

    # 解析每个房子的网页信息
    def ershou_parse(self, response):
        """这是二手房的解析"""
        html_data = response.text
        etree_html = etree.HTML(html_data)
        # 得到详情链接
        house_id = etree_html.xpath('//ul[@class="sellListContent"]//li[@class="clear LOGVIEWDATA LOGCLICKDATA"]//div[@class="info clear"]/div[@class="title"]/a/@data-housecode')
        street = etree_html.xpath('//ul[@class="sellListContent"]//li[@class="clear LOGVIEWDATA LOGCLICKDATA"]//div[@class="info clear"]//div[@class="flood"]/div[@class="positionInfo"]/a[2]/text()')
        xiaoqu = etree_html.xpath('//ul[@class="sellListContent"]//li[@class="clear LOGVIEWDATA LOGCLICKDATA"]//div[@class="info clear"]//div[@class="flood"]/div[@class="positionInfo"]/a[1]/text()')
        xiaoqu = [i.strip(' ') for i in xiaoqu]
        prices = etree_html.xpath('//ul[@class="sellListContent"]//li[@class="clear LOGVIEWDATA LOGCLICKDATA"]//div[@class="info clear"]//div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()')
        detail_link = etree_html.xpath('//ul[@class="sellListContent"]//li[@class="clear LOGVIEWDATA LOGCLICKDATA"]//div[@class="info clear"]/div[@class="title"]/a/@href')
        area = etree_html.xpath('//div[@class="bigImgList"]//div[@class="item"]//div[@class="info"]/text()')
        area = ['%.2f' % float(i.rstrip('平米')) for i in area if '平米' in i]
        for idx in range(len(house_id)):
            item = LianjiaItem()
            item['house_id'] = house_id[idx]
            item['county'] = self.area[0]
            item['street'] = street[idx]
            item['xiaoqu'] = xiaoqu[idx]
            item['price'] = prices[idx]
            item['area'] = area[idx]
            item['detail_link'] = detail_link[idx]
            yield item

    def new_house_parse(self, response):
        html_data = response.text
        etree_html = etree.HTML(html_data)
        house_id = etree_html.xpath(
            '//ul[@class="resblock-list-wrapper"]//li[@class="resblock-list post_ulog_exposure_scroll"]/@data-project-name')
        street = etree_html.xpath(
            '//ul[@class="resblock-list-wrapper"]//li[@class="resblock-list post_ulog_exposure_scroll"]//div[@class="resblock-location"]/span[2]/text()')
        xiaoqu = etree_html.xpath(
            '//ul[@class="resblock-list-wrapper"]//li[@class="resblock-list post_ulog_exposure_scroll"]//div[@class="resblock-desc-wrapper"]//div[@class="resblock-name"]/a[class="name"]/text()')
        xiaoqu = [i.strip(' ') for i in xiaoqu]
        avg_prices = etree_html.xpath(
            '//ul[@class="resblock-list-wrapper"]//li[@class="resblock-list post_ulog_exposure_scroll"]//div[@class="resblock-price"]//div[@class="main-price"]/span/text()')
        areas = etree_html.xpath('//ul[@class="resblock-list-wrapper"]//li[@class="resblock-list post_ulog_exposure_scroll"]//div[@class="resblock-area"]//span/text()')
        new_area = []
        for i in areas:
            new_area.append(re.sub(r'[^0-9]', '', i))
        prices = [int(i[0])*int(i[1]) for i in zip(avg_prices, new_area)]  # 根据面积和单机，计算总价
        detail_link = etree_html.xpath(
            '//ul[@class="resblock-list-wrapper"]//li[@class="resblock-list post_ulog_exposure_scroll"]//div[@class="resblock-desc-wrapper"]//div[@class="resblock-name"]/a[class="name"]/@href')

        for idx in range(len(house_id)):
            item = LianjiaItem()
            item['house_id'] = house_id[idx]
            item['county'] = self.area[0]
            item['street'] = street[idx]
            item['xiaoqu'] = xiaoqu[idx]
            item['price'] = prices[idx]
            item['area'] = new_area[idx]
            item['detail_link'] = detail_link[idx]
            yield item