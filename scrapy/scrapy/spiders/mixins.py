# -*- coding: utf-8 -*-

from scrapy.urls import pluviometro
import scrapy


class APACSpiderMixin(scrapy.Spider):
    allowed_domains = [pluviometro.get('domain'), ]
    start_urls = [pluviometro.get('home'), ]
