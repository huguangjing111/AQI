# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from datetime import datetime
from scrapy.exporters import CsvItemExporter

import pymongo
import redis
import json


class AqiPipeline(object):
    def process_item(self, item, spider):
        # item["crawl_time"] = str(datetime.utcnow())
        # item["source"] = spider.name
        return item


class AqiCsvPipeline(object):
    def open_spider(self, spider):
        # 保存csv数据的文件对象
        self.f = open("aqi.csv", "w")
        # 创建csv文件读写对象
        self.csv_exporter = CsvItemExporter(self.f)
        # 开始进行csv文件读写
        self.csv_exporter.start_exporting()

    def process_item(self, item, spider):
        # 每次写入一个item数据
        self.csv_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        # 结束csv文件读写
        self.csv_exporter.finish_exporting()
        # 关闭文件
        self.f.close()


class AqiJsonPipeline(object):
    def open_spider(self, spider):
        self.f = open("aqi.json", "w")
        self.f.write("[\n")

    def process_item(self, item, spider):
        content = json.dumps(dict(item)) + ",\n"
        print content
        print '======================================'
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.write("]")
        self.f.close()


class AqiMongoPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        self.db = self.client["AQI"]
        self.collection = self.db["aqi"]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class AqiRedisPipeline(object):
    def open_spider(self, spider):
        self.client = redis.Redis(host="127.0.0.1", port=6379)

    def process_item(self, item, spider):
        content = json.dumps(dict(item))
        self.client.lpush("aqi", content)
        return item


class AqiMySQLPipeline(object):
    pass







