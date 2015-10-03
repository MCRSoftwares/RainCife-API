# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy_djangoitem import DjangoItem
from .items import MarkerItem


class TakeFirstPipeline(object):
    def process_item(self, item, spider):
        for name, value in item.items():
            item[name] = value[0]
        return item


class SaveMarkerModelPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, DjangoItem):
            if not MarkerItem.django_model.objects.filter(
                    apac_id=int(item['apac_id'])).exists():
                return item.save()
        return item
