# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from AQI.items import AqiItem


class AqispiderSpider(RedisSpider):
    name = 'aqiredisspider'
    allowed_domains = ['aqistudy.cn']
    # start_urls = ['https://www.aqistudy.cn/historydata/']
    redis_key = "aqiredisspider:start_urls"

    # 起始页
    def parse(self, response):
        # 所有的城市列表的href
        monthdata_href_list = response.xpath('//div[@class="all"]//ul//a/@href')[:3]
        for monthdata_href in monthdata_href_list:
            item = AqiItem()
            url = 'https://www.aqistudy.cn/historydata/' + monthdata_href.extract()
            item['city'] = url[55:]
            # print(url)
            yield scrapy.Request(url,callback=self.parse_monthdata, meta={'item': item})

    # 月份详情页
    def parse_monthdata(self, response):
        # item = response.meta['item']
        # 跳转的每日详情页href
        daydata_href_list = response.xpath('//tbody/tr/td[1]/a/@href')[:3]
        if not len(daydata_href_list):
            return
        for daydata_href in daydata_href_list:
            url = 'https://www.aqistudy.cn/historydata/' + daydata_href.extract()
            yield scrapy.Request(url, callback=self.parse_daydata, meta=response.meta)

    # 每日详情页
    def parse_daydata(self,response):
        item = response.meta['item']
        node_list = response.xpath('//tbody/tr')
        node_list.pop(0)
        if not len(node_list):
            return
        for node in node_list:
            # 日期
            item['date'] = node.xpath('td[1]/text()').extract_first()
            # AQI
            item['AQI'] = node.xpath('td[2]/text()').extract_first()
            # 质量等级
            item['quality_rank'] = node.xpath('td[3]//text()').extract_first()
            # pm 2.5
            item['PM_25'] = node.xpath('td[4]/text()').extract_first()
            # pm 10
            item['PM_10'] = node.xpath('td[5]/text()').extract_first()
            # so2
            item['SO2'] = node.xpath('td[6]/text()').extract_first()
            # co
            item['CO'] = node.xpath('td[7]/text()').extract_first()
            # no2
            item['NO2'] = node.xpath('td[8]/text()').extract_first()
            # O3
            item['O3'] = node.xpath('td[9]/text()').extract_first()

            yield item
