# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TelantPipeline(object):
    def process_item(self, item, spider):
        return item

import pymongo

class DevicePipeline(object):

    collection_name = 'device_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri='mongodb://localhost:27017/',
            mongo_db='ipran'
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.client.drop_database('ipran')
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if 'tl_network_layer' in item:
            self.db[self.collection_name].insert(dict(item))
        return item

class DeviceErrorPipeline(object):
    collection_name = 'device_error_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri='mongodb://localhost:27017/',
            mongo_db='ipran'
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if 'device_exception' in item:
            self.db[self.collection_name].insert(dict(item))
        return item

class CardPipeline(object):
    collection_name = 'card_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri='mongodb://localhost:27017/',
            mongo_db='ipran'
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if 'tl_is_motherboard' in item:
            self.db[self.collection_name].insert(dict(item))
        return item

class CardErrorPipeline(object):
    collection_name = 'card_error_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri='mongodb://localhost:27017/',
            mongo_db='ipran'
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if 'card_exception' in item:
            self.db[self.collection_name].insert(dict(item))
        return item

class LinkPipeline(object):
    collection_name = 'link_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri='mongodb://localhost:27017/',
            mongo_db='ipran'
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if 'tl_optical_code' in item:
            self.db[self.collection_name].insert(dict(item))
        return item

class LinkErrorPipeline(object):
    collection_name = 'link_error_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri='mongodb://localhost:27017/',
            mongo_db='ipran'
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if 'link_exception' in item:
            self.db[self.collection_name].insert(dict(item))
        return item
