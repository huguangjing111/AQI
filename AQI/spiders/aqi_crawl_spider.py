#coding:utf-8

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from AQI.items import AqiItem


class AqiCrawlSpider(CrawlSpider):
    name = "aqicrawlspider4"
    allowed_domains = ["aqistudy.cn"]
    start_urls = ["https://www.aqistudy.cn/historydata/"]

    rules = [
        Rule(LinkExtractor(allow=r"monthdata\.php\?city="), follow=True),
        Rule(LinkExtractor(allow=r"daydata\.php\?city=.+?&month=\d+-\d+"), callback="parse_day")
    ]

    def parse_day(self, response):
        node_list = response.xpath("//div[@class='row']//tbody/tr")
        city_name = response.xpath("//h2[@id='title']/text()").extract_first()

        if not len(node_list):
            return

        node_list.pop(0)

        for node in node_list:
            # item = AqiItem()
            item = {}
            #item["city"] = response.meta["city"]
            item["city"] = city_name[8:-11]
            item["date"] = node.xpath("./td[1]//text()").extract_first()
            item["aqi"] = node.xpath("./td[2]//text()").extract_first()
            item["level"] = node.xpath("./td[3]//text()").extract_first()
            item["pm2_5"] = node.xpath("./td[4]//text()").extract_first()
            item["pm10"] = node.xpath("./td[5]//text()").extract_first()
            item["so2"] = node.xpath("./td[6]//text()").extract_first()
            item["co"] = node.xpath("./td[7]//text()").extract_first()
            item["no2"] = node.xpath("./td[8]//text()").extract_first()
            item["o3"] = node.xpath("./td[9]//text()").extract_first()

            yield item
