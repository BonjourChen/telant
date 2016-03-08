# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DeviceItem(scrapy.Item):
    tl_meid = scrapy.Field()
    tl_name = scrapy.Field()
    tl_assemblename = scrapy.Field()
    tl_telnet_ip = scrapy.Field()
    tl_model = scrapy.Field()
    tl_vendor = scrapy.Field()
    tl_role = scrapy.Field()
    tl_network_layer = scrapy.Field()
    tl_speciality = scrapy.Field()
    tl_circlecode = scrapy.Field()
    tl_cityname = scrapy.Field()
    tl_region = scrapy.Field()
    tl_marketing_area = scrapy.Field()
    tl_room = scrapy.Field()
    tl_project_status = scrapy.Field()
    tl_life_status = scrapy.Field()
    tl_typespec_id = scrapy.Field()

class CardItem(scrapy.Item):
    tl_device_meid = scrapy.Field()
    tl_typespec_id = scrapy.Field()
    tl_device_telnet_ip = scrapy.Field()
    tl_is_mothreboard = scrapy.Field()
    tl_physical_code = scrapy.Field()
    tl_logic_code = scrapy.Field()
    tl_shelf_code = scrapy.Field()
    tl_total_portcount = scrapy.Field()
    tl_occupy_portcount = scrapy.Field()
    tl_free_portcount = scrapy.Field()
    tl_using_status = scrapy.Field()
    tl_alias = scrapy.Field()
    tl_speciality = scrapy.Field()
    tl_device_model = scrapy.Field()
    tl_model = scrapy.Field()
    tl_standard_name = scrapy.Field()
    tl_standard_code = scrapy.Field()
    tl_category = scrapy.Field()
    tl_room = scrapy.Field()
    tl_vendor = scrapy.Field()
    tl_device_name = scrapy.Field()
    tl_wg_code = scrapy.Field()
    tl_region = scrapy.Field()
    tl_life_status = scrapy.Field()
    tl_physical_status = scrapy.Field()
    tl_project_status = scrapy.Field()
    tl_work_way = scrapy.Field()

class CardErrorItem(scrapy.Item):
    tl_device_meid = scrapy.Field()
    tl_typespec_id = scrapy.Field()
    tl_device_telnet_ip = scrapy.Field()
    tl_device_name = scrapy.Field()
    response_body = scrapy.Field()
