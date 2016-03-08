# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import scrapy
import json
import logging
import re
from telant.items import *

#  logging.log(logging.DEBUG, "This is a warning")

class TelantSpider(scrapy.Spider):
    name = "Telant"
    allowed_domains = ["132.121.96.108:8001/telant"]
    start_urls = (
        'http://132.121.96.108:8001/telant/',
    )

    #  def start_requests(self):
        #  return [scrapy.FormRequest("http://132.121.96.108:8001/telant/",
                                   #  method = "POST",
                                   #  formdata={
                                       #  "lt":"LT-72257-aYDAWkPiJ6jIl6loCjPIUkhYWgvOUW",
                                       #  "execution":"e1s1",
                                       #  "_eventId":"submit",
                                       #  "_secondAuthentication":"",
                                       #  "loginFromSubApp":"",
                                       #  "username":"SA",
                                       #  "password":"321EWQ"
                                   #  },
                                   #  callback=self.logged_in)]

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
            "username":"SA",
            "password":"321EWQ"
        }
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36',
            'Cookie':cookie
        }
        #  print formdata, headers

        #  yield scrapy.FormRequest.from_response(
        #  response,
        #  formdata={
        #  "username":"SA",
        #  "password":"321EWQ"
        #  },
        #  headers={
        #  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36',
        #  'Cookie':cookie
        #  },
        #  callback = self.logged_in,
        #  dont_filter = True
        #  )
        yield scrapy.FormRequest("http://132.121.96.108:8001/cas/login?service=http%3A%2F%2F132.121.96.108%3A8001%2Ftelant%2Fpage%2Flogin.jsp",
                                 method = "POST",
                                 headers= headers,
                                 formdata = formdata,
                                 callback=self.parse_test,
                                 dont_filter=True)

    def parse_test(self, response):
        cookie = response.headers['Set-Cookie'].partition(';')[0]
        url = 'http://132.121.96.108:8001/telant/security_check'

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
        url = 'http://132.121.96.108:8001/telant/dorado/view-service'
        body = '''<batch>
<request type="json"><![CDATA[{"action":"load-data","dataProvider":"deviceMgr#doLoadData","supportsEntity":true,"parameter":{"__viewConfigName":"com.ccssoft.inventory.web.equipment.view.DeviceMgr","CUS_FILTER":null,"metaClassName":"ROUTER","CUS_OWNER_NET_ID":"23","isCollection":"true","isTemplate":null,"paramValue":"23","cus_specId":"1024600001","CUS_SPEC":"路由器"},"resultDataType":"v:com.ccssoft.inventory.web.equipment.view.DeviceMgr$[v:com.ccssoft.inventory.web.equipment.view.DeviceMgr$dataTypeEntity]","pageSize":100,"pageNo":1,"context":{},"loadedDataTypes":["dataTypeCondition","dataTypeSpec","dataTypeEntity","dataTypeOwnerNet","dataSetSS__SS","dataTypeNumber","dataTypeSharding","dataSetIMS__AGCF","datatypeSwitchLog","dataSetVPNNUMBER__VPNNUMBER"]}]]></request>
</batch>'''
        request = scrapy.Request(
            url, method='POST',
            body=body,
            headers={'Content-Type':'text/xml'},
            callback=self.parse_device1,
            dont_filter=True
        )
        yield request

    def parse_device1(self, response):
        #  scrapy.shell.inspect_response(response, self)
        tmp = response.body
        pageCount = int( re.search(r'"pageCount":(\d+)', tmp).group(1) )
        if pageCount >= 1:
            for idx in range( pageCount ):
                url = 'http://132.121.96.108:8001/telant/dorado/view-service'
                body = '''<batch>
        <request type="json"><![CDATA[{"action":"load-data","dataProvider":"deviceMgr#doLoadData","supportsEntity":true,"parameter":{"__viewConfigName":"com.ccssoft.inventory.web.equipment.view.DeviceMgr","CUS_FILTER":null,"metaClassName":"ROUTER","CUS_OWNER_NET_ID":"23","isCollection":"true","isTemplate":null,"paramValue":"23","cus_specId":"1024600001","CUS_SPEC":"路由器"},"resultDataType":"v:com.ccssoft.inventory.web.equipment.view.DeviceMgr$[v:com.ccssoft.inventory.web.equipment.view.DeviceMgr$dataTypeEntity]","pageSize":100,"pageNo":''' + str(idx+1) + ''',"context":{},"loadedDataTypes":["dataTypeCondition","dataTypeSpec","dataTypeEntity","dataTypeOwnerNet","dataSetSS__SS","dataTypeNumber","dataTypeSharding","dataSetIMS__AGCF","datatypeSwitchLog","dataSetVPNNUMBER__VPNNUMBER"]}]]></request>
        </batch>'''
                request = scrapy.Request(
                    url, method='POST',
                    body=body,
                    headers={'Content-Type':'text/xml'},
                    callback=self.parse_device2,
                    dont_filter=True
                )
                yield request

    def parse_device2(self, response):
        #  scrapy.shell.inspect_response(response, self)
        if response.status == 200:
            tmp = response.body
            data = re.search(r'^{$.*^}$', tmp, re.S | re.M).group(0)
            jsonData = json.loads(data)['data']['data']
            for tmpData in jsonData:
                Item = DeviceItem()
                Item['tl_meid'] = tmpData.setdefault('ID', '')
                Item['tl_name'] = tmpData.setdefault('NM_CODE', '')
                Item['tl_assemblename'] = tmpData.setdefault('NAME', '')
                Item['tl_telnet_ip'] = tmpData.setdefault('TELNET_IP', '')
                Item['tl_model'] = tmpData.setdefault('TYPE_DEVICE_CONTAIN_ROUTER@NAME', '')
                Item['tl_vendor'] = tmpData.setdefault('VENDOR_CONTAIN_ROUTER@NAMECN', '')
                Item['tl_role'] = tmpData.setdefault('CUS_SPEC', '')
                Item['tl_network_layer'] = tmpData.setdefault('NETWORK_LAYER_ID', '')
                Item['tl_speciality'] = tmpData.setdefault('OWNER_NET_ID', '')
                Item['tl_circlecode'] = tmpData.setdefault('CIRCLE_NAME', '')
                Item['tl_cityname'] = tmpData.setdefault('DEVICE_BIND_SHARDING_1@NAME', '')
                Item['tl_region'] = tmpData.setdefault('SMALL_COUNTRY', '')
                Item['tl_marketing_area'] = tmpData.setdefault('MARKETING_AREA', '')
                Item['tl_room'] = tmpData.setdefault('CUS_ENTITY_ROOM', '')
                Item['tl_project_status'] = tmpData.setdefault('PROJECT_STATUS_ID', '')
                Item['tl_life_status'] = tmpData.setdefault('LIFE_STATE_ID', '')
                Item['tl_typespec_id'] = tmpData.setdefault('TYPE_DEVICE_CONTAIN_ROUTER@TYPESPEC_ID', '')
                yield Item

                url = 'http://132.121.96.108:8001/telant/dorado/view-service'
                body = '''
<batch>
<request type="json"><![CDATA[{"action":"load-data","dataProvider":"cardMgr#queryCardParamService","supportsEntity":true,"parameter":{"parentMetaClassName":"''' + str( Item['tl_typespec_id'] ) + '''","__viewConfigName":"com.ccssoft.inventory.web.equipment.view.CardParameterAndServiceMgr","metaClassName":"CARD","isCollection":"true","parentEntityId":"''' + str( Item['tl_meid'] ) + '''","paramValue":null,"deviceMetaClassName":null,"deviceEntityId":null},"resultDataType":"v:com.ccssoft.inventory.web.equipment.view.CardParameterAndServiceMgr$[v:com.ccssoft.inventory.web.equipment.view.CardParameterAndServiceMgr$dataTypeEntity]","pageSize":100,"pageNo":1,"context":{},"loadedDataTypes":["dataTypeEntity","dataTypeLifeState","dataTypeSanYuanZu","dataTypeSvlan","dataTypeCondition","dataTypeCardRate","dataTypeCardType"]}]]></request>
</batch>
                '''
                request = scrapy.Request(
                    url, method='POST',
                    body=body,
                    headers={'Content-Type':'text/xml'},
                    callback=self.parse_card,
                    dont_filter=True
                )
                request.meta['Item'] = Item
                yield request

    def parse_card(self, response):
        #  scrapy.shell.inspect_response(response, self)
        tmp = response.body
        deviceItem = response.meta['Item']
        try:
            data = re.search(r'^{$.*^}$', tmp, re.S | re.M).group(0)
            #  jsonData = json.loads(data)['data']['data'][0]
            jsonData = json.loads(data)['data']['data']
            for tmpData in jsonData:
                Item = CardItem()
                Item['tl_device_meid'] = deviceItem['tl_meid']
                Item['tl_typespec_id'] = deviceItem['tl_typespec_id']
                Item['tl_device_telnet_ip'] = deviceItem['tl_telnet_ip']
                Item['tl_is_mothreboard'] = tmpData.setdefault("isMotherBoard", '')
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
        except:
            #  scrapy.shell.inspect_response(response, self)
            Item = CardErrorItem()
            Item['tl_device_meid'] = deviceItem['tl_meid']
            Item['tl_typespec_id'] = deviceItem['tl_typespec_id']
            Item['tl_device_telnet_ip'] = deviceItem['tl_telnet_ip']
            Item['tl_device_name'] = deviceItem['tl_name']
            Item['response_body'] = response.body
            yield Item
