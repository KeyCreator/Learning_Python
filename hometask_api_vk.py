import requests
from urllib.parse import urlencode
from pprint import pprint

APP_ID = 7302563
AUTH_URL, AUTH_VERSION = 'https://oauth.vk.com/authorize', 5.52
USERS_URL, USERS_VERSION = 'https://api.vk.com/method/users.get', 5.89
FRIENDS_URL, FRIENDS_VERSION = 'https://api.vk.com/method/friends.get', 5.8
TOKEN = 'b9615847d62cea0ba3f865a7fa4b17072babfaeb27e43b67d3e0b053d7d65239a9b026aaed733ab6ef755'
USER1_ID = '392477722'
USER2_ID = '209762'
VK_URL = 'https://vk.com/'

def get_url_for_token():

    params = {
        "client_id": APP_ID,
        'display': 'page',
        'scope': 'status,friends',
        'response_type': 'token',
        'v': AUTH_VERSION
    }
    return '?'.join((AUTH_URL, urlencode(params)))

def get_user_name(token, user_id):

    params = {
        'access_token': token,
        'user_ids': user_id,
        'fields': 'domain',
        'v': USERS_VERSION,
    }
    response = requests.get(
        USERS_URL,
        params
    ).json()

    if 'error' in response.keys():
        return  
    else:
        return response['response'][0]['first_name'],\
               response['response'][0]['last_name'], \
               VK_URL+response['response'][0]['domain']

class User:
    def __new__(cls, token, user_id):
        print(f'  Checking the validity of the user ID {user_id}')
        
        if not get_user_name(token, user_id):
            raise ValueError(f'The specified token "{token}" or user "{user_id}" is not valid') 
            return  
        else:
            print('  Ok')
            return super().__new__(cls)

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id
        self.first_name, self.last_name, self.vk_url = get_user_name(token, user_id)

    def __and__(self, other):
        print('  Geting set of user1 friends')
        set1 = set(foo['id'] for foo in self.get_friends()['response']['items'])
        print('  Geting set of user2 friends')
        set2 = set(foo['id'] for foo in other.get_friends()['response']['items'])
        #print(f'the IDs of the mutual friends: {set1 & set2}')
        return [User(self.token, foo) for foo in (set1 & set2)]

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.vk_url}'

    def get_params(self):
        return {
            'access_token': self.token,
            'user_id': self.user_id,
            'order': 'name',
            'fields': 'nickname',
            'v': FRIENDS_VERSION,
        }

    def get_friends(self):
        params = self.get_params()     
        response = requests.get(
            FRIENDS_URL,
            params
        )
        return response.json()

if __name__ == '__main__':

    user_choice = input('Press 1 to get the token. Press 2 if you already have a token. Press other - end the program: ').strip()
    if user_choice == '1':
        print('Click the link to get the token. Copy the received token to the clipboard')
        print(get_url_for_token())
    elif user_choice == '2':
        token, user1_id, user2_id = \
               input('  Please enter the token (Enter - token in the last test): ').strip(), \
               input(f'  Please enter user1 ID (Enter - {USER1_ID}): ').strip(), \
               input(f'  Please enter user2 ID (Enter - {USER2_ID}): ').strip()

        # Default values for testing
        if token == '': token = TOKEN
        if user1_id == '': user1_id = USER1_ID
        if user2_id == '': user2_id = USER2_ID

        user1 = User(token, user1_id)  
        user2 = User(token, user2_id)

        print('Getting the IDs of the mutual friends:')
        [print(foo) for foo in (user1 & user2)]
              
