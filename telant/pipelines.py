# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from telant.items import *

class DevicePipeline(object):

    collection_name = 'device_items'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        if spider.name == 'telant_ipran':
            self.client.drop_database('ipran')
            self.db = self.client['ipran']
        elif spider.name == 'telant_man':
            self.client.drop_database('man')
            self.db = self.client['man']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item.__class__ is DeviceItem:
            self.db[self.collection_name].insert(dict(item))
        return item

class DeviceErrorPipeline(object):
    collection_name = 'device_error_items'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        if spider.name == 'telant_ipran':
            self.db = self.client['ipran']
        elif spider.name == 'telant_man':
            self.db = self.client['man']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item.__class__ is DeviceErrorItem:
            self.db[self.collection_name].insert(dict(item))
        return item

class CardPipeline(object):
    collection_name = 'card_items'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        if spider.name == 'telant_ipran':
            self.db = self.client['ipran']
        elif spider.name == 'telant_man':
            self.db = self.client['man']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item.__class__ is CardItem:
            self.db[self.collection_name].insert(dict(item))
        return item

class CardErrorPipeline(object):
    collection_name = 'card_error_items'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        if spider.name == 'telant_ipran':
            self.db = self.client['ipran']
        elif spider.name == 'telant_man':
            self.db = self.client['man']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item.__class__ is CardErrorItem:
            self.db[self.collection_name].insert(dict(item))
        return item

class LinkPipeline(object):
    collection_name = 'link_items'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        if spider.name == 'telant_ipran':
            self.db = self.client['ipran']
        elif spider.name == 'telant_man':
            self.db = self.client['man']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item.__class__ is LinkItem:
            self.db[self.collection_name].insert(dict(item))
        return item

class LinkErrorPipeline(object):
    collection_name = 'link_error_items'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        if spider.name == 'telant_ipran':
            self.db = self.client['ipran']
        elif spider.name == 'telant_man':
            self.db = self.client['man']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item.__class__ is LinkErrorItem:
            self.db[self.collection_name].insert(dict(item))
        return item
