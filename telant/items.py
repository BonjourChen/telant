# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DeviceItem(scrapy.Item):
    tl_meid = scrapy.Field()
    tl_name = scrapy.Field()
    tl_code = scrapy.Field()
    tl_ems_name = scrapy.Field()
    tl_standard_name = scrapy.Field()
    tl_standard_code = scrapy.Field()
    tl_assemblename = scrapy.Field()
    tl_telnet_ip = scrapy.Field()
    tl_model = scrapy.Field()
    tl_vendor = scrapy.Field()
    tl_speciality = scrapy.Field()
    tl_network_layer = scrapy.Field()
    tl_role = scrapy.Field()
    tl_owner_net = scrapy.Field()
    tl_circlecode = scrapy.Field()
    tl_cityname = scrapy.Field()
    tl_region = scrapy.Field()
    tl_marketing_area = scrapy.Field()
    tl_room = scrapy.Field()
    tl_project_status = scrapy.Field()
    tl_life_status = scrapy.Field()
    tl_typespec_id = scrapy.Field()
    tl_create_date = scrapy.Field()
    tl_modify_date = scrapy.Field()

class DeviceErrorItem(scrapy.Item):
    device_exception = scrapy.Field()
    response_body = scrapy.Field()

class CardItem(scrapy.Item):
    tl_device_meid = scrapy.Field()
    tl_device_typespec_id = scrapy.Field()
    tl_device_telnet_ip = scrapy.Field()
    tl_is_motherboard = scrapy.Field()
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
    tl_device_typespec_id = scrapy.Field()
    tl_device_telnet_ip = scrapy.Field()
    tl_device_name = scrapy.Field()
    card_exception = scrapy.Field()
    response_body = scrapy.Field()

class LinkItem(scrapy.Item):
    tl_device_meid = scrapy.Field()
    tl_device_telnet_ip = scrapy.Field()
    tl_device_name = scrapy.Field()
    tl_service_name = scrapy.Field()
    tl_last_order_code = scrapy.Field()
    tl_access_code = scrapy.Field()
    tl_using_status = scrapy.Field()
    tl_a_room = scrapy.Field()
    tl_a_device_name = scrapy.Field()
    tl_a_device_meid = scrapy.Field()
    tl_a_port_name = scrapy.Field()
    tl_z_room = scrapy.Field()
    tl_z_device_name = scrapy.Field()
    tl_z_device_meid = scrapy.Field()
    tl_z_port_name = scrapy.Field()
    tl_optical_code = scrapy.Field()

class LinkErrorItem(scrapy.Item):
    tl_device_meid = scrapy.Field()
    tl_device_telnet_ip = scrapy.Field()
    tl_device_name = scrapy.Field()
    link_exception = scrapy.Field()
    response_body = scrapy.Field()
