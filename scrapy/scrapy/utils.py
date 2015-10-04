# -*- coding: utf-8 -*-


class Urls(object):
    urls = None
    domain = None

    def __init__(self, *args, **kwargs):
        if not self.urls:
            raise NotImplementedError('No URL list given.')

        if not self.domain:
            raise NotImplementedError('No domain given.')

        self._url_list = generate_urls(domain=self.domain, urls=self.urls)
        super(Urls, self).__init__(*args, **kwargs)

    def get(self, url_name):
        return self._url_list[url_name]


def generate_urls(domain, urls={}):
    _urls = {
        'domain': domain,
        'http': 'http://www.{0}'.format(domain),
    }

    for name, url in urls.items():
        _urls[name] = '{{0}}{0}'.format(url).format(_urls['http'])

    return _urls
