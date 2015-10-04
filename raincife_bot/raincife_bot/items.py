# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from apac.models import APACMarker


class MarkerItem(DjangoItem):
    django_model = APACMarker