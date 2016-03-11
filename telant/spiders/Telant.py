# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import scrapy
import json
import logging
import re
from telant.items import *

class TelantSpider(scrapy.Spider):
    name = "Telant"
    allowed_domains = ["132.121.92.224:8803/telant"]
    start_urls = (
        'http://132.121.92.224:8803/telant/',
    )

    def parse(self, response):
        cookie = response.headers['Set-Cookie'].partition(';')[0]
        lt = response.xpath('//input[@name="lt"]/@value').extract()[0]
        execution = response.xpath('//input[@name="execution"]/@value').extract()[0]
        formdata={
            "lt":lt,
            "execution":execution,
            "_eventId":"submit",
            "_secondAuthentication":"",
            "loginFromSubApp":"",
            "username":"guoyy2",
            "password":"123qwe!Q"
        }
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36',
            'Cookie':cookie
        }
        yield scrapy.FormRequest("http://132.121.92.224:8813/cas/login?service=http%3A%2F%2F132.121.92.224%3A8803%2Ftelant%2Fpage%2Flogin.jsp",
                                 method = "POST",
                                 headers= headers,
                                 formdata = formdata,
                                 callback=self.parse_transit,
                                 dont_filter=True)

    def parse_transit(self, response):
        cookie = response.headers['Set-Cookie'].partition(';')[0]
        url = 'http://132.121.92.224:8803/telant/security_check'

        yield scrapy.Request(
            url = url,
            method = 'POST',
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36',
                'Cookie':cookie
            },
            callback = self.logged_in,
            dont_filter=True
        )

    def logged_in(self, response):
        url = 'http://132.121.92.224:8803/telant/dorado/view-service'
        body = '''
<batch>
<request type="json"><![CDATA[{"action":"load-data","dataProvider":"deviceMgr#doLoadData","supportsEntity":true,"parameter":{"__viewConfigName":"com.ccssoft.inventory.web.equipment.view.DeviceMgr","CUS_FILTER":null,"metaClassName":"ROUTER","CUS_OWNER_NET_ID":"23","isCollection":"true","isTemplate":null,"paramValue":"23","cus_specId":"1024600001","CUS_SPEC":"路由器"},"resultDataType":"v:com.ccssoft.inventory.web.equipment.view.DeviceMgr$[v:com.ccssoft.inventory.web.equipment.view.DeviceMgr$dataTypeEntity]","pageSize":100,"pageNo":1,"context":{},"loadedDataTypes":["dataTypeCondition","dataTypeSpec","dataTypeEntity","dataTypeOwnerNet","dataSetSS__SS","dataTypeNumber","dataTypeSharding","dataSetIMS__AGCF","datatypeSwitchLog","dataSetVPNNUMBER__VPNNUMBER"]}]]></request>
</batch>'''
        request = scrapy.Request(
            url, method='POST',
            body=body,
            headers={'Content-Type':'text/xml'},
            callback=self.parse_device,
            dont_filter=True
        )
        yield request

    def parse_device(self, response):
        tmp = response.body
        try:
            pageCount = int( re.search(r'"pageCount":(\d+)', tmp).group(1) )
            pageNo = int( re.search(r'"pageNo":(\d+)', tmp).group(1) )
            data = re.search(r'^{$.*^}$', tmp, re.S | re.M).group(0)
            jsonData = json.loads(data)['data']['data']

            url = 'http://132.121.92.224:8803/telant/dorado/view-service'
            for tmpData in jsonData:
                Item = DeviceItem()
                Item['tl_meid'] = tmpData.setdefault('ID', '')
                Item['tl_name'] = tmpData.setdefault('NAME', '')
                Item['tl_code'] = tmpData.setdefault('CODE', '')
                Item['tl_ems_name'] = tmpData.setdefault('NM_CODE', '')
                Item['tl_standard_name'] = tmpData.setdefault("STANDARD_NAME", '')
                Item['tl_standard_code'] = tmpData.setdefault("STANDARD_CODE", '')
                Item['tl_assemblename'] = tmpData.setdefault('NAME', '')
                Item['tl_telnet_ip'] = tmpData.setdefault('TELNET_IP', '')
                Item['tl_model'] = tmpData.setdefault('TYPE_DEVICE_CONTAIN_ROUTER@NAME', '')
                Item['tl_vendor'] = tmpData.setdefault('VENDOR_CONTAIN_ROUTER@NAMECN', '')
                Item['tl_speciality'] = tmpData.setdefault('CUS_SPEC', '')
                Item['tl_network_layer'] = tmpData.setdefault('NETWORK_LAYER_ID', '')
                Item['tl_role'] = tmpData.setdefault('NETWORK_ROLE_ID', '')
                Item['tl_owner_net'] = tmpData.setdefault('OWNER_NET_ID', '')
                Item['tl_circlecode'] = tmpData.setdefault('CIRCLE_NAME', '')
                Item['tl_cityname'] = tmpData.setdefault('DEVICE_BIND_SHARDING_1@NAME', '')
                Item['tl_region'] = tmpData.setdefault('SMALL_COUNTRY', '')
                Item['tl_marketing_area'] = tmpData.setdefault('MARKETING_AREA', '')
                Item['tl_room'] = tmpData.setdefault('CUS_ENTITY_ROOM', '')
                Item['tl_project_status'] = tmpData.setdefault('PROJECT_STATUS_ID', '')
                Item['tl_life_status'] = tmpData.setdefault('LIFE_STATE_ID', '')
                Item['tl_typespec_id'] = tmpData.setdefault('TYPE_DEVICE_CONTAIN_ROUTER@TYPESPEC_ID', '')
                Item['tl_create_date'] = tmpData.setdefault('CREATE_DATE', '')
                Item['tl_modify_date'] = tmpData.setdefault('MODIFY_DATE', '')
                yield Item

                body_card = '''
<batch>
<request type="json"><![CDATA[{"action":"load-data","dataProvider":"cardMgr#queryCardParamService","supportsEntity":true,"parameter":{"parentMetaClassName":"''' + str( Item['tl_typespec_id'] ) + '''","__viewConfigName":"com.ccssoft.inventory.web.equipment.view.CardParameterAndServiceMgr","metaClassName":"CARD","isCollection":"true","parentEntityId":"''' + str( Item['tl_meid'] ) + '''","paramValue":null,"deviceMetaClassName":null,"deviceEntityId":null},"resultDataType":"v:com.ccssoft.inventory.web.equipment.view.CardParameterAndServiceMgr$[v:com.ccssoft.inventory.web.equipment.view.CardParameterAndServiceMgr$dataTypeEntity]","pageSize":100,"pageNo":1,"context":{},"loadedDataTypes":["dataTypeEntity","dataTypeLifeState","dataTypeSanYuanZu","dataTypeSvlan","dataTypeCondition","dataTypeCardRate","dataTypeCardType"]}]]></request>
</batch>
'''
                request_card = scrapy.Request(
                    url, method='POST',
                    body=body_card,
                    headers={'Content-Type':'text/xml'},
                    callback=self.parse_card,
                    dont_filter=True
                )
                request_card.meta['Item'] = Item
                yield request_card

                body_link = '''
<batch>
<request type="json"><![CDATA[{"action":"load-data","dataProvider":"businessMgr#doLoadData","supportsEntity":true,"parameter":{"isCollection":"true","entityId":"''' + str(Item['tl_meid']) + '''","className":"DEVICE","type":"inside"},"resultDataType":"v:com.ccssoft.inventory.web.equipment.view.BusinessMgr$[v:com.ccssoft.inventory.web.equipment.view.BusinessMgr$dtInside]","pageSize":50,"pageNo":1,"context":{},"loadedDataTypes":["dtWithOutProLink","dtInside","dtInsert","dtRent"]}]]></request>
</batch>
'''
                request_link = scrapy.Request(
                    url, method='POST',
                    body=body_link,
                    headers={'Content-Type':'text/xml'},
                    callback=self.parse_link,
                    dont_filter=True
                )
                request_link.meta['Item'] = Item
                yield request_link
            if pageCount > pageNo:
                body_device = '''
<batch>
<request type="json"><![CDATA[{"action":"load-data","dataProvider":"deviceMgr#doLoadData","supportsEntity":true,"parameter":{"__viewConfigName":"com.ccssoft.inventory.web.equipment.view.DeviceMgr","CUS_FILTER":null,"metaClassName":"ROUTER","CUS_OWNER_NET_ID":"23","isCollection":"true","isTemplate":null,"paramValue":"23","cus_specId":"1024600001","CUS_SPEC":"路由器"},"resultDataType":"v:com.ccssoft.inventory.web.equipment.view.DeviceMgr$[v:com.ccssoft.inventory.web.equipment.view.DeviceMgr$dataTypeEntity]","pageSize":100,"pageNo":''' + str(pageNo + 1) + ''',"context":{},"loadedDataTypes":["dataTypeCondition","dataTypeSpec","dataTypeEntity","dataTypeOwnerNet","dataSetSS__SS","dataTypeNumber","dataTypeSharding","dataSetIMS__AGCF","datatypeSwitchLog","dataSetVPNNUMBER__VPNNUMBER"]}]]></request>
</batch>'''
                request_device = scrapy.Request(
                    url, method='POST',
                    body=body_device,
                    headers={'Content-Type':'text/xml'},
                    callback=self.parse_device,
                    dont_filter=True
                )
                yield request_device
        #  捕捉re正则的异常，担心设备有时候查询错误(但是经实践好像没有)，获取的response不符合所写的正则
        except Exception as e:
            #  scrapy.shell.inspect_response(response, self)
            Item = DeviceErrorItem()
            Item['device_exception'] = str(e)
            Item['response_body'] = response.body
            yield Item

    def parse_card(self, response):
        #  scrapy.shell.inspect_response(response, self)
        tmp = response.body
        deviceItem = response.meta['Item']
        try:
            data = re.search(r'^{$.*^}$', tmp, re.S | re.M).group(0)
            pageCount = int( re.search(r'"pageCount":(\d+)', tmp).group(1) )
            pageNo = int( re.search(r'"pageNo":(\d+)', tmp).group(1) )
            jsonData = json.loads(data)['data']['data']
            for tmpData in jsonData:
                Item = CardItem()
                Item['tl_device_meid'] = deviceItem['tl_meid']
                Item['tl_device_typespec_id'] = deviceItem['tl_typespec_id']
                Item['tl_device_telnet_ip'] = deviceItem['tl_telnet_ip']
                Item['tl_is_motherboard'] = tmpData.setdefault("isMotherBoard", '')
                Item['tl_physical_code'] = tmpData.setdefault("CUS_SLOT_NAME", '')
                Item['tl_logic_code'] = tmpData.setdefault("CUS_SLOT_CODE", '')
                Item['tl_shelf_code'] = tmpData.setdefault("CUS_SHELF_CODE", '')
                Item['tl_total_portcount'] = tmpData.setdefault("PORTCOUNT_TOTAL", '')
                Item['tl_occupy_portcount'] = tmpData.setdefault("PORTCOUNT_OCCUPY", '')
                Item['tl_free_portcount'] = tmpData.setdefault("PORTCOUNT_FREE", '')
                Item['tl_using_status'] = tmpData.setdefault("USING_STATE_ID", '')
                Item['tl_alias'] = tmpData.setdefault("ALIAS", '')
                Item['tl_speciality'] = tmpData.setdefault("BELONG_SPECIALITY_ID", '')
                Item['tl_device_model'] = tmpData.setdefault("NAME", '')
                Item['tl_model'] = tmpData.setdefault("TYPE_CARD_CONTAIN_CARD@MODEL", '')
                Item['tl_standard_name'] = tmpData.setdefault("STANDARD_NAME", '')
                Item['tl_standard_code'] = tmpData.setdefault("STANDARD_CODE", '')
                Item['tl_category'] = tmpData.setdefault("CUS_CARD_CATEGORY", '')
                Item['tl_room'] = tmpData.setdefault("FACILITY_HOLD_WARE@NAME", '')
                Item['tl_vendor'] = tmpData.setdefault("VENDOR_CONTAIN_CARD@NAMECN", '')
                Item['tl_device_name'] = tmpData.setdefault("DEVICE_CONTAIN_WARE@NAME", '')
                Item['tl_wg_code'] = tmpData.setdefault("NM_CODE", '')
                Item['tl_region'] = tmpData.setdefault("SHARDING_ID", '')
                Item['tl_life_status'] = tmpData.setdefault("LIFE_STATE_ID", '')
                Item['tl_physical_status'] = tmpData.setdefault("PHYSICAL_STATE_ID", '')
                Item['tl_project_status'] = tmpData.setdefault("PROJECT_STATUS_ID", '')
                Item['tl_work_way'] = tmpData.setdefault("WORK_WAY_ID", '')
                yield Item
            if pageCount > pageNo:
                url = 'http://132.121.92.224:8803/telant/dorado/view-service'
                body_card = '''
<batch>
<request type="json"><![CDATA[{"action":"load-data","dataProvider":"cardMgr#queryCardParamService","supportsEntity":true,"parameter":{"parentMetaClassName":"''' + str( deviceItem['tl_typespec_id'] ) + '''","__viewConfigName":"com.ccssoft.inventory.web.equipment.view.CardParameterAndServiceMgr","metaClassName":"CARD","isCollection":"true","parentEntityId":"''' + str( deviceItem['tl_meid'] ) + '''","paramValue":null,"deviceMetaClassName":null,"deviceEntityId":null},"resultDataType":"v:com.ccssoft.inventory.web.equipment.view.CardParameterAndServiceMgr$[v:com.ccssoft.inventory.web.equipment.view.CardParameterAndServiceMgr$dataTypeEntity]","pageSize":100,"pageNo":''' + str(pageNo + 1) + '''',"context":{},"loadedDataTypes":["dataTypeEntity","dataTypeLifeState","dataTypeSanYuanZu","dataTypeSvlan","dataTypeCondition","dataTypeCardRate","dataTypeCardType"]}]]></request>
</batch>
'''
                request_card = scrapy.Request(
                    url, method='POST',
                    body=body_card,
                    headers={'Content-Type':'text/xml'},
                    callback=self.parse_card,
                    dont_filter=True
                )
                request_card.meta['Item'] = deviceItem
                yield request_card
        #  捕捉re正则的异常，板卡有时候查询错误，获取的response不符合所写的正则
        except Exception as e:
            #  scrapy.shell.inspect_response(response, self)
            Item = CardErrorItem()
            Item['tl_device_meid'] = deviceItem['tl_meid']
            Item['tl_device_typespec_id'] = deviceItem['tl_typespec_id']
            Item['tl_device_telnet_ip'] = deviceItem['tl_telnet_ip']
            Item['tl_device_name'] = deviceItem['tl_ems_name']
            Item['card_exception'] = str(e)
            Item['response_body'] = response.body
            yield Item


    def parse_link(self, response):
        #  scrapy.shell.inspect_response(response, self)
        tmp = response.body
        deviceItem = response.meta['Item']
        try:
            data = re.search(r'^{$.*^}$', tmp, re.S | re.M).group(0)
            pageCount = int( re.search(r'"pageCount":(\d+)', tmp).group(1) )
            pageNo = int( re.search(r'"pageNo":(\d+)', tmp).group(1) )
            try:
                jsonData = json.loads(data)['data']['data']
            #  捕捉json转换时候的异常，因为链路(板卡不会)有些编码问题会导致json转换的时候出错，遇到这种response对body解码就行了
            except ValueError as e1:
                #  logging.warning("This is a warning:" + str(e1))
                try:
                    jsonData = json.loads(data.decode("unicode-escape"))['data']['data']
                except ValueError as e2:
                    #  logging.warning("This is a warning:" + str(e2))
                    #后面字符串的锅  "REQUIREMENT_DESC":""南溪综合机房\/RAN-A-6(ZXCTN 6130XG-S)'1\/8---跳纤---- 南溪综合机房\/LTEENODEB10 07槽 UMPT板第一端口"",
                    jsonData = json.loads(re.sub(r'(?<!:)""|""(?!,)', '"', data.decode("unicode-escape")), strict = False)['data']['data']
            finally:
                for tmpData in jsonData:
                    Item = LinkItem()
                    Item['tl_device_meid'] = deviceItem['tl_meid']
                    Item['tl_device_telnet_ip'] = deviceItem['tl_telnet_ip']
                    Item['tl_device_name'] = deviceItem['tl_ems_name']
                    Item['tl_service_name'] = tmpData.setdefault("NAME", '')
                    Item['tl_last_order_code'] = tmpData.setdefault("LAST_ORDER_CODE", '')
                    Item['tl_access_code'] = tmpData.setdefault("ACCESS_CODE", '')
                    Item['tl_using_status'] = tmpData.setdefault("usingState", '')
                    Item['tl_a_room'] = tmpData.setdefault("SERVICE_END_A_FACILITY@NAME", '')
                    Item['tl_a_device_name'] = tmpData.setdefault("aDeviceName", '')
                    Item['tl_a_device_meid'] = tmpData.setdefault("SERVICE_END_A_PORT@PHYSIC_DEVICE_ID", '')
                    Item['tl_a_port_name'] = tmpData.setdefault("aPortName", '')
                    Item['tl_z_room'] = tmpData.setdefault("SERVICE_END_Z_FACILITY@NAME", '')
                    Item['tl_z_device_name'] = tmpData.setdefault("zDeviceName", '')
                    Item['tl_z_device_meid'] = tmpData.setdefault("SERVICE_END_Z_PORT@PHYSIC_DEVICE_ID", '')
                    Item['tl_z_port_name'] = tmpData.setdefault("zPortName", '')
                    Item['tl_optical_code'] = tmpData.setdefault("fibersectionCode", '')
                    yield Item
                if pageCount > pageNo:
                    url = 'http://132.121.92.224:8803/telant/dorado/view-service'
                    body_link = '''
<batch>
<request type="json"><![CDATA[{"action":"load-data","dataProvider":"businessMgr#doLoadData","supportsEntity":true,"parameter":{"isCollection":"true","entityId":"''' + str(deviceItem['tl_meid']) + '''","className":"DEVICE","type":"inside"},"resultDataType":"v:com.ccssoft.inventory.web.equipment.view.BusinessMgr$[v:com.ccssoft.inventory.web.equipment.view.BusinessMgr$dtInside]","pageSize":50,"pageNo":''' + str(pageNo + 1) + ''',"context":{},"loadedDataTypes":["dtWithOutProLink","dtInside","dtInsert","dtRent"]}]]></request>
</batch>
'''
                    request_link = scrapy.Request(
                        url, method='POST',
                        body=body_link,
                        headers={'Content-Type':'text/xml'},
                        callback=self.parse_link,
                        dont_filter=True
                    )
                    request_link.meta['Item'] = deviceItem
                    yield request_link
        #  捕捉re正则的异常，担心链路有时候查询错误(但是经实践好像没有)，获取的response不符合所写的正则
        except Exception as e:
            Item = LinkErrorItem()
            Item['tl_device_meid'] = deviceItem['tl_meid']
            Item['tl_device_telnet_ip'] = deviceItem['tl_telnet_ip']
            Item['tl_device_name'] = deviceItem['tl_ems_name']
            Item['link_exception'] = str(e)
            Item['response_body'] = response.body
            yield Item
