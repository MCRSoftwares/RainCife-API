# -*- coding: utf-8 -*-

from .handlers import SensorListHandler
from .handlers import SensorCreateHandler
from .handlers import SensorRetrieveHandler


apac_patterns = [
    (r'/api/v1/sensores/', SensorListHandler),
    (r'/api/v1/sensores/([0-9]+)/', SensorRetrieveHandler),
    (r'/api/v1/sensores/criar/', SensorCreateHandler),
]
