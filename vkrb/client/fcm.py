import logging

from vkrb.client.base import BaseClient, Methods

logger = logging.getLogger(__name__)


class FirebaseClient(BaseClient):
    BASE_URL = 'https://fcm.googleapis.com/'

    def check_response(self, response):
        return response.status_code == 200

    def success_handler(self, response):
        logger.info('success firebase response %s', response.json())
        return super().success_handler(response.json())

    def error_handler(self, response):
        logger.info('error firebase response %s', response.text)
        return response


class NotificationFirebaseMethod(FirebaseClient):
    method = 'fcm/send'
    http_method = Methods.POST

    def __init__(self, key, to=None, registration_ids=None, data=None,
                 notification=None):
        assert to or type(registration_ids) == list
        assert notification or data
        assert key
        self.to = to
        self.registration_ids = registration_ids
        self.key = key
        self.data = data
        self.notification = notification

    def get_headers(self):
        return {
            'Authorization': f'key={self.key}'
        }

    def get_params(self):
        params = {
            'content_available': True
        }

        if self.data:
            params['data'] = self.data

        if self.notification:
            params['notification'] = self.notification

        if self.to:
            params['to'] = self.to
        elif self.registration_ids:
            params['registration_ids'] = self.registration_ids

        return params
