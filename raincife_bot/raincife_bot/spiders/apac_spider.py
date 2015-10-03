# -*- coding: utf-8 -*-

from scrapy.http import FormRequest
from raincife_bot.urls import pluviometro
from .mixins import APACSpiderMixin


class APACBaseDataSpider(APACSpiderMixin):
    name = 'apac_base_data'

    def parse(self, response):
        form_data = {
            'acao': 'exibePluviometrosRMRSite',
            'local': '-1'
        }
        return FormRequest(pluviometro.get('data'), formdata=form_data,
                           callback=self.parse_xhrequest)

    def parse_xhrequest(self, response):
        # TODO Crawlear dados de chuva
        pass
