# -*- coding: utf-8 -*-
import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")

import scrapy
import json
import logging
import re

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
        #  scrapy.shell.inspect_response(response, self)
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
        #  url = 'http://132.121.96.108:8001/telant/com.ccssoft.inventory.web.equipment.view.DeviceMgr.d7?metaClassName=ROUTER&CUS_OWNER_NET_ID=23&templateIndicator=23'
        url = 'http://132.121.96.108:8001/telant/dorado/view-service'
        body = '''<batch>
<request type="json"><![CDATA[{"action":"load-data","dataProvider":"deviceMgr#doLoadData","supportsEntity":true,"parameter":{"__viewConfigName":"com.ccssoft.inventory.web.equipment.view.DeviceMgr","CUS_FILTER":null,"metaClassName":"ROUTER","CUS_OWNER_NET_ID":"23","isCollection":"true","isTemplate":null,"paramValue":"23","cus_specId":"1024600001","CUS_SPEC":"路由器"},"resultDataType":"v:com.ccssoft.inventory.web.equipment.view.DeviceMgr$[v:com.ccssoft.inventory.web.equipment.view.DeviceMgr$dataTypeEntity]","pageSize":100,"pageNo":1,"context":{},"loadedDataTypes":["dataTypeCondition","dataTypeSpec","dataTypeEntity","dataTypeOwnerNet","dataSetSS__SS","dataTypeNumber","dataTypeSharding","dataSetIMS__AGCF","datatypeSwitchLog","dataSetVPNNUMBER__VPNNUMBER"]}]]></request>
</batch>'''
        #  body = '''<batch>
#  <request type="json"><![CDATA[{"action":"load-data","dataProvider":"businessMgr#doLoadData","supportsEntity":true,"parameter":{"isCollection":"true","entityId":"441000000000001006301400","className":"DEVICE","type":"inside"},"resultDataType":"v:com.ccssoft.inventory.web.equipment.view.BusinessMgr$[v:com.ccssoft.inventory.web.equipment.view.BusinessMgr$dtInside]","pageSize":50,"pageNo":1,"context":{},"loadedDataTypes":["dtRent","dtWithOutProLink","dtInsert","dtInside"]}]]></request>
#  </batch>'''
        request = scrapy.Request(
            url, method='POST', 
            body=body,
            headers={'Content-Type':'text/xml'},
            callback=self.parse_test2,
            dont_filter=True
        )
        yield request

    def parse_test2(self, response):
        #  with open('test.html', 'w') as f:
            #  f.write(response.body)
        #  scrapy.shell.inspect_response(response, self)
        tmp = response.body
        data = re.search(r'^{$.*^}$', tmp, re.S | re.M).group(0)
        with open('test.json', 'w') as f:
            f.write(data)

