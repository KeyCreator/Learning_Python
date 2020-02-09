import requests
from urllib.parse import urlencode
from pprint import pprint

APP_ID = 7302563
AUTH_URL = 'https://oauth.vk.com/authorize'
oparams = {
    "client_id": APP_ID,
    'display': 'page',
    'scope': 'status',
    'response_type': 'token',
    'v': 5.52
}

##print('?'.join((AUTH_URL, urlencode(oparams))))

TOKEN = '35fac83eac91eb752f58da07ec1364724ca1a418e2b5982fe89d68573d213c86f3dec9a3baf0c0787bca2'


params = {
    'access_token': TOKEN,
    'v': 5.52,
    'text': 'Foo & Bar'
}

response = requests.get(
    'https://api.vk.com/method/status.set',
    params
)


##params = {
##    'access_token': TOKEN,
##    'v': 5.52,    
##}
##
##response = requests.get(
##    'https://api.vk.com/method/status.get',
##    params
##)

pprint(response.json())

##class User:
##    def __init__(self, token):
##        self.token = token
##
##    def get_params(self):
##        return {
##            'access_token': TOKEN,
##            'v': 5.52,
##        }
##
##    def get_status(self):
##        params = self.get_params()
##        response = requests.get(
##            'https://api.vk.com/method/status.get',
##            params
##        )
##        return response.json()
##
##    def set_status(self):
##        params = self.get_params()
##        params['text'] = text
##        response = requests.get(
##            'https://api.vk.com/method/status.set',
##            params
##        )
##        return response.json()
##
####print('?'.join((AUTH_URL, urlencode(oparams))))
##sergey = User(TOKEN)
##status = sergey.get_status()
##print(status)
