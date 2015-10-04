# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.urls import pluviometro
from .mixins import APACSpiderMixin
from scrapy.items import MarkerItem
import time


class APACMarkersSpider(APACSpiderMixin):
    name = 'apac_markers'

    def parse(self, response):
        return Request(pluviometro.get('markers'),
                       callback=self.parse_xhrequest)

    def parse_xhrequest(self, response):
        for marker in response.xpath('//markers/marker'):
            item = MarkerItem()
            item.update({
                'apac_id': marker.xpath('@mon_estacao_id').extract(),
                'name': marker.xpath('@mon_estacao_nome').extract(),
                'local': marker.xpath('@mon_estacao_local').extract(),
                'latitude': marker.xpath('@mon_estacao_latitude').extract(),
                'longitude': marker.xpath('@mon_estacao_longitude').extract(),
            })
            time.sleep(0.5)
            yield item
