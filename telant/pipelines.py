# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import pymysql
import pymysql.cursors
from scrapy import log
from telant.items import *
from twisted.enterprise import adbapi

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

class MySQLDevicePipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode= True)
        dbpool = adbapi.ConnectionPool('pymysql',**dbargs)
        return cls(dbpool)

    def open_spider(self,spider):
        if spider.name == 'telant_ipran':
            self.dbpool.runOperation('TRUNCATE TABLE tl_ipran_device_items')
        elif spider.name == 'telant_man':
            self.dbpool.runOperation('TRUNCATE TABLE tl_man_device_items')

    def process_item(self,item,spider):
        if spider.name == 'telant_ipran':
            query = self.dbpool.runInteraction(self._conditional_insert, item, 'tl_ipran_device_items')
        elif spider.name == 'telant_man':
            query = self.dbpool.runInteraction(self._conditional_insert, item, 'tl_man_device_items')
        return item

    def _conditional_insert(self,tx,item,table_name):
        if item.__class__ is DeviceItem:
            tx.execute(\
                "INSERT INTO " + table_name + " (tl_ems_name, tl_role, tl_tml_area, tl_cityname,"
                    "tl_speciality,tl_small_country,tl_project_status,tl_code,tl_typespec_id,tl_specification,tl_meid,tl_network_layer,tl_room,"
                    "tl_assemblename,tl_reg_area,tl_vendor,tl_standard_code,tl_circlecode,tl_modify_date,"
                    "tl_owner_net,tl_name,tl_life_status,tl_standard_name,tl_create_date,tl_telnet_ip,tl_marketing_area,"
                    "tl_model,syndate) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,SYSDATE())",(
                    str(item['tl_ems_name']),str(item['tl_role']),str(item['tl_tml_area']),str(item['tl_cityname']),
                    str(item['tl_speciality']),str(item['tl_small_country']),str(item['tl_project_status']),str(item['tl_code']),
                    str(item['tl_typespec_id']),str(item['tl_specification']),str(item['tl_meid']),str(item['tl_network_layer']),str(item['tl_room']),str(item['tl_assemblename']),
                    str(item['tl_reg_area']),str(item['tl_vendor']),str(item['tl_standard_code']),str(item['tl_circlecode']),
                    str(item['tl_modify_date']),str(item['tl_owner_net']),str(item['tl_name']),str(item['tl_life_status']),
                    str(item['tl_standard_name']),str(item['tl_create_date']),str(item['tl_telnet_ip']),str(item['tl_marketing_area']),
                    str(item['tl_model'])))

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

class MySQLDeviceErrorPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode= True)
        dbpool = adbapi.ConnectionPool('pymysql',**dbargs)
        return cls(dbpool)

    def open_spider(self,spider):
        if spider.name == 'telant_ipran':
            self.dbpool.runOperation('TRUNCATE TABLE tl_ipran_device_error_items')
        elif spider.name == 'telant_man':
            self.dbpool.runOperation('TRUNCATE TABLE tl_man_device_error_items')

    def process_item(self,item,spider):
        if spider.name == 'telant_ipran':
            query = self.dbpool.runInteraction(self._conditional_insert, item, 'tl_ipran_device_error_items')
        elif spider.name == 'telant_man':
            query = self.dbpool.runInteraction(self._conditional_insert, item, 'tl_man_device_error_items')
        return item

    def _conditional_insert(self,tx,item,table_name):
        if item.__class__ is DeviceErrorItem:
            tx.execute(\
                "INSERT INTO " + table_name + " (device_exception,response_body,syndate) values(%s,%s,SYSDATE())",(
                    str(item['device_exception']),str(item['response_body'])))

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

class MySQLCardPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode= True)
        dbpool = adbapi.ConnectionPool('pymysql',**dbargs)
        return cls(dbpool)

    def open_spider(self,spider):
        if spider.name == 'telant_ipran':
            self.dbpool.runOperation('TRUNCATE TABLE tl_ipran_card_items')
        elif spider.name == 'telant_man':
            self.dbpool.runOperation('TRUNCATE TABLE tl_man_card_items')

    def process_item(self,item,spider):
        if spider.name == 'telant_ipran':
            query = self.dbpool.runInteraction(self._conditional_insert, item, 'tl_ipran_card_items')
        elif spider.name == 'telant_man':
            query = self.dbpool.runInteraction(self._conditional_insert, item, 'tl_man_card_items')
        return item

    def _conditional_insert(self,tx,item,table_name):
        if item.__class__ is CardItem:
            tx.execute(\
                "INSERT INTO " + table_name + "(tl_device_meid,tl_device_typespec_id,tl_device_telnet_ip,tl_is_motherboard,"
                "tl_physical_code,tl_logic_code,tl_shelf_code,tl_total_portcount,tl_occupy_portcount,"
                "tl_free_portcount,tl_using_status,tl_alias,tl_speciality,tl_device_model,tl_model,"
                "tl_standard_name,tl_standard_code,tl_category,tl_room,tl_vendor,tl_device_name,tl_wg_code,"
                "tl_region,tl_life_status,tl_physical_status,tl_project_status,tl_work_way,syndate) values"
                "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,SYSDATE())",(str(item['tl_device_meid']),
                    str(item['tl_device_typespec_id']),str(item['tl_device_telnet_ip']),str(item['tl_is_motherboard']),str(item['tl_physical_code']),
                    str(item['tl_logic_code']),str(item['tl_shelf_code']),str(item['tl_total_portcount']),str(item['tl_occupy_portcount']),
                    str(item['tl_free_portcount']),str(item['tl_using_status']),str(item['tl_alias']),str(item['tl_speciality']),
                    str(item['tl_device_model']),str(item['tl_model']),str(item['tl_standard_name']),str(item['tl_standard_code']),
                    str(item['tl_category']),str(item['tl_room']),str(item['tl_vendor']),str(item['tl_device_name']),str(item['tl_wg_code']),
                    str(item['tl_region']),str(item['tl_life_status']),str(item['tl_physical_status']),str(item['tl_project_status']),
                    str(item['tl_work_way'])))

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

class MySQLCardErrorPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode= True)
        dbpool = adbapi.ConnectionPool('pymysql',**dbargs)
        return cls(dbpool)

    def open_spider(self,spider):
        if spider.name == 'telant_ipran':
            self.dbpool.runOperation('TRUNCATE TABLE tl_ipran_card_error_items')
        elif spider.name == 'telant_man':
            self.dbpool.runOperation('TRUNCATE TABLE tl_man_card_error_items')

    def process_item(self,item,spider):
        if spider.name == 'telant_ipran':
            query = self.dbpool.runInteraction(self._conditional_insert, item, 'tl_ipran_card_error_items')
        elif spider.name == 'telant_man':
            query = self.dbpool.runInteraction(self._conditional_insert, item, 'tl_man_card_error_items')
        return item

    def _conditional_insert(self,tx,item,table_name):
        if item.__class__ is CardErrorItem:
            tx.execute(\
                "INSERT INTO " + table_name + "(tl_device_meid,tl_device_typespec_id,tl_device_telnet_ip,"
                "tl_device_name,card_exception,response_body,syndate) values"
                "(%s,%s,%s,%s,%s,%s,SYSDATE())",(str(item['tl_device_meid']),str(item['tl_device_typespec_id']),
                str(item['tl_device_telnet_ip']),str(item['tl_device_name']),str(item['card_exception']),str(item['response_body'])))

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

class MySQLLinkPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode= True)
        dbpool = adbapi.ConnectionPool('pymysql',**dbargs)
        return cls(dbpool)

    def open_spider(self,spider):
        if spider.name == 'telant_ipran':
            self.dbpool.runOperation('TRUNCATE TABLE tl_ipran_link_items')
        elif spider.name == 'telant_man':
            self.dbpool.runOperation('TRUNCATE TABLE tl_man_link_items')

    def process_item(self,item,spider):
        if spider.name == 'telant_ipran':
            query = self.dbpool.runInteraction(self._conditional_insert, item, 'tl_ipran_link_items')
        elif spider.name == 'telant_man':
            query = self.dbpool.runInteraction(self._conditional_insert, item, 'tl_man_link_items')
        return item

    def _conditional_insert(self,tx,item,table_name):
        if item.__class__ is LinkItem:
            tx.execute(\
                "INSERT INTO " + table_name + "(tl_device_meid,tl_device_telnet_ip,tl_device_name,tl_service_name,tl_last_order_code,"
                "tl_access_code,tl_using_status,tl_a_room,tl_a_device_name,tl_a_device_meid,tl_a_port_name,tl_z_room,tl_z_device_name,"
                "tl_z_device_meid,tl_z_port_name,tl_optical_code,syndate) values"
                "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,SYSDATE())",(str(item['tl_device_meid']),str(item['tl_device_telnet_ip']),
                    str(item['tl_device_name']),str(item['tl_service_name']),str(item['tl_last_order_code']),str(item['tl_access_code']),
                    str(item['tl_using_status']),str(item['tl_a_room']),str(item['tl_a_device_name']),str(item['tl_a_device_meid']),
                    str(item['tl_a_port_name']),str(item['tl_z_room']),str(item['tl_z_device_name']),str(item['tl_z_device_meid']),
                    str(item['tl_z_port_name']),str(item['tl_optical_code'])))

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

class MySQLLinkErrorPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode= True)
        dbpool = adbapi.ConnectionPool('pymysql',**dbargs)
        return cls(dbpool)

    def open_spider(self,spider):
        if spider.name == 'telant_ipran':
            self.dbpool.runOperation('TRUNCATE TABLE tl_ipran_link_error_items')
        elif spider.name == 'telant_man':
            self.dbpool.runOperation('TRUNCATE TABLE tl_man_link_error_items')

    def process_item(self,item,spider):
        if spider.name == 'telant_ipran':
            query = self.dbpool.runInteraction(self._conditional_insert, item, 'tl_ipran_link_error_items')
        elif spider.name == 'telant_man':
            query = self.dbpool.runInteraction(self._conditional_insert, item, 'tl_man_link_error_items')
        return item

    def _conditional_insert(self,tx,item,table_name):
        if item.__class__ is LinkErrorItem:
            tx.execute(\
                "INSERT INTO " + table_name + "(tl_device_meid,tl_device_telnet_ip,tl_device_name,link_exception,response_body,"
                "syndate) values (%s,%s,%s,%s,%s,SYSDATE())",(str(item['tl_device_meid']),str(item['tl_device_telnet_ip']),
                str(item['tl_device_name']),str(item['link_exception']),str(item['response_body'])))