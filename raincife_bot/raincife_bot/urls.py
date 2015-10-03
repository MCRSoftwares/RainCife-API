# -*- coding: utf-8 -*-

from .utils import Urls


class Pluviometro(Urls):
    domain = 'apac.pe.gov.br'
    urls = {
        'home': '/meteorologia/chuvas-rmr.php',
        'data': '/_lib/pluviometria.request.php',
        'markers': '/meteorologia/gera-xml-pluviometros-rmr_novo.php',
    }


pluviometro = Pluviometro()
