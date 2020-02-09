from pprint import pprint
from typing import Any

import requests
from urllib.parse import urlencode

APP_ID = 6975433
BASE_URL = 'https://oauth.vk.com/authorize'
auth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'response_type': 'token',
    'scope': 'status',
    'v': '5.95',
    'redirect_uri': 'https://example.com/'
}

# print('?'.join((BASE_URL, urlencode(auth_data))))

TOKEN = '75cd5ae1dc61c9c851ef36220f0f2a0ae5a74cbce876e2be58f9c3047ce9ebc6d6f699c7a234692f8c539'

params = {
    'access_token': TOKEN,
    'v': '5.95'
}


class User:
    def __init__(self, token, first_name=None, last_name=None):
        self.token = token
        self.first_name = first_name
        self.last_name = last_name

    def get_params(self):
        return dict(
            access_token=self.token,
            v='5.95'
        )

    def get_info(self):
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        self.first_name = response.json()['response'][0]['first_name']
        self.last_name = response.json()['response'][0]['last_name']
        return response.json()

    def get_status(self):
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/status.set',
            params
        )
        return response.json()

    def set_status(self, text):
        params = self.get_params()
        params['text'] = text
        response = requests.get(
            'https://api.vk.com/method/status.set',
            params
        )
        return response.json()


artyom = User(TOKEN)
artyom.get_info()
print(artyom.first_name, artyom.last_name)
