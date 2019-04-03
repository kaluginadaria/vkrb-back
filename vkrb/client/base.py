from enum import Enum

import requests


class Methods(Enum):
    GET = 'get'
    HEAD = 'head'
    POST = 'post'
    PATCH = 'patch'
    PUT = 'put'
    DELETE = 'delete'
    OPTIONS = 'options'


class BaseClient:
    BASE_URL = None
    METHODS = Methods

    method = None
    http_method = None

    def get_params(self):
        return {}

    def get_headers(self):
        return {}

    @classmethod
    def generate_url(cls, method):
        return '{0}{1}'.format(cls.BASE_URL, method)

    def _get_data(self, method, http_method):
        request = getattr(requests, http_method.value)
        kwargs = {}
        if self.get_params():
            if http_method == Methods.GET:
                kwargs['params'] = self.get_params()
            else:
                kwargs['json'] = self.get_params()
        if self.get_headers():
            kwargs['headers'] = self.get_headers()
        response = request(self.generate_url(method), **kwargs)
        if self.check_response(response):
            return self.success_handler(response)
        return self.error_handler(response)

    def check_response(self, response):
        return True

    def success_handler(self, response):
        return response

    def error_handler(self, response):
        return response

    def execute(self):
        return self._get_data(self.method, self.http_method)
