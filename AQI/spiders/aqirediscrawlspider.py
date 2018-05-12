# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

from AQI.items import AqiItem


class AqispiderSpider(RedisCrawlSpider):
    name = 'aqirediscrawlspider'
    allowed_domains = ['aqistudy.cn']
    # start_urls = ['https://www.aqistudy.cn/historydata/']
    redis_key = "aqirediscrawlspider:start_urls"

    rules = [
        Rule(LinkExtractor(allow=r"monthdata\.php\?city="), follow=True),
        Rule(LinkExtractor(allow=r"daydata\.php\?city=.+?&month=\d+-\d+"), callback="parse_daydata")
    ]

    # 每日详情页
    def parse_daydata(self, response):
        item = AqiItem
        node_list = response.xpath('//tbody/tr')
        city_name = response.xpath("//h2[@id='title']/text()").extract_first()
        node_list.pop(0)
        if not len(node_list):
            return
        for node in node_list:
            item["city"] = city_name[8:-11]
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
