# -*- coding: utf-8 -*-

from django.db import models


class APACMarker(models.Model):
    apac_id = models.IntegerField()
    name = models.CharField(max_length=128)
    local = models.CharField(max_length=128)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=18, decimal_places=15)

    def __unicode__(self):
        return u'({0}) {1} - {2}'.format(self.apac_id, self.local, self.name)

    class Meta:
        verbose_name = 'APAC Marker'
        verbose_name_plural = 'APAC Markers'
