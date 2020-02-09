import requests
from urllib.parse import urlencode
from pprint import pprint
import time
import json

APP_ID = 7302563
AUTH_URL, AUTH_VERSION = 'https://oauth.vk.com/authorize', 5.52
USERS_URL, USERS_VERSION = 'https://api.vk.com/method/users.get', 5.89
FRIENDS_URL, FRIENDS_VERSION = 'https://api.vk.com/method/friends.get', 5.8
GROUPS_URL, GROUPS_VERSION = 'https://api.vk.com/method/groups.get', 5.61
GROUP_URL, GROUP_VERSION = 'https://api.vk.com/method/groups.getById', 5.61
TOKEN = '37ad712c17fcb20d11c18576f3e4d795fde75dce825cc28abfd7b22ea7ecaf3c1d08bef69de950b2b8778'
USER_ID = '392477722'
##USER_ID = '209762'
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

def get_group_dict(token, group_id):

    params = {
            'access_token': token,
            'group_id': group_id,
            'fields': 'name,members_count',
            'v': GROUP_VERSION,
    }
    response = requests.get(
           GROUP_URL,
           params
    ).json()
    return response['response'][0]


class User(object):

    def __init__(self, token, user_id):
        self.user_id = user_id
        self.token = token

        self.params_friends = {
            'access_token': token,
            'user_id': user_id,
            'order': 'name',
            'fields': 'nickname',
            'v': FRIENDS_VERSION,
        }

        self.params_groups = {
            'access_token': token,
            'user_id': user_id,
            'extended': '0',
            'v': FRIENDS_VERSION,
        }

    @property
    def friends_ids(self):
        response = requests.get(
            FRIENDS_URL,
            self.params_friends
        ).json()
        return set([foo['id'] for foo in response['response']['items']])

    @property    
    def groups_ids(self):
        response = requests.get(
            GROUPS_URL,
            self.params_groups
        ).json()
        return set(response['response']['items'])

if __name__ == '__main__':

    user_choice = input('Press 1 to get the token. Press 2 if you already have a token. Press other - end the program: ').strip()

    if user_choice == '1':
        
        print('Click the link to get the token. Copy the received token to the clipboard')
        print(get_url_for_token())
        
    elif user_choice == '2':

        token, user_id = \
               input('  Please enter the token (Enter - token in the last test): ').strip(), \
               input(f'  Please enter user1 ID (Enter - {USER_ID}): ').strip()

        # Default values for testing
        if token == '': token = TOKEN
        if user_id == '': user_id = USER_ID

        user = User(token, user_id)
        print('Friends: ', type(user.friends_ids))
        print(user.friends_ids)

        result = user.groups_ids

        print('Groups: ', type(result))
        print(result)
        
        for friend_id in user.friends_ids:
            time.sleep(0.3)
            
            friend = User(token, friend_id)

            try:
                friend_groups = friend.groups_ids
            except:
                print(f'Error User_ID: {friend_id}')
                continue
            
            print(f'Friend_ID: {friend.user_id}, him groups: {friend_groups}')
            result -= friend_groups

        print('Program result:')
        print(result)        
        data = []
        with open('output.json', 'w') as file:
            for foo in result:
                item = get_group_dict(token, foo)
                data.append({
                    'name': item['name'],
                    'gid': item['id'],
                    'members_count': item['members_count'],                    
                })
            json.dump(data, file, ensure_ascii=False, indent=4)

##[
##    {
##    “name”: “Название группы”, 
##    “gid”: “идентификатор группы”, 
##    “members_count”: количество_участников_сообщества
##    },
##    {
##    …
##    }
##]
