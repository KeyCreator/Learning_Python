'''
Вопросы преподавателю:
    1) Что нужно переделать, чтобы код был более "питоническим"?
    2) Я сделал глобальную переменную errors - корзину, куда помещаю ошибки возникшие во время выполнения разных функций.
        Затем записываю содержимое "корзины" в файл errors.txt.
        Насколько это правильное решение?
    4) Почему работа под моим токеном выдает больше ошибок, чем работа под заданным токеном?

Что нужно реализовать:
    1) Использовать execute для ускорения работы
    2) Показывать прогресс процентами
    3) Восстанавливается если случился ReadTimeout
    4) Показывать в том числе группы, в которых есть общие друзья, но не более, чем N человек, где N задается в коде.
    5) Если у пользователя больше 1000 групп, можно ограничиться первой тысячей

Что реализовано:
1) класс User
2) класс Group
3) основной алгоритм задачи (вычитание множеств)
4) выгрузка результата в файл
5) Имя пользователя в качесвте входных данных
6) Выводить ошибки в отдельный файл с описанием ошибки
7) ПОказывать процесс точками

'''


import requests
from urllib.parse import urlencode
import time
import json

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
AUTH_URL, AUTH_VERSION = 'https://oauth.vk.com/authorize', 5.52
USERS_URL, USERS_VERSION = 'https://api.vk.com/method/users.get', 5.89
FRIENDS_URL, FRIENDS_VERSION = 'https://api.vk.com/method/friends.get', 5.8
GROUPS_URL, GROUPS_VERSION = 'https://api.vk.com/method/groups.get', 5.61
GROUP_URL, GROUP_VERSION = 'https://api.vk.com/method/groups.getById', 5.61
VK_URL = 'https://vk.com/'

USER_ID = '392477722'
##USER_ID = '209762'

DELAY = 0.4

errors = []

def check_valid_user_id(token, user_id):
    params = {
        'access_token': token,
        'user_ids': user_id,
        'v': USERS_VERSION
    }
    response = requests.get(
        USERS_URL,
        params
    ).json()

    if 'error' in response: return
    
    return response['response'][0]['id']

class Group():

    def __init__(self, token, group_id):
        self.group_id = group_id
        self.token = token
        self.params_group = {
            'access_token': token,
            'group_id': group_id,
            'fields': 'name,members_count',
            'v': GROUP_VERSION
        }
        
    @property
    def data(self):

        response = requests.get(
            GROUP_URL,
            self.params_group
        ).json()
 
        return {
            'name': response['response'][0]['name'],
            'gid': response['response'][0]['id'],
            'members_count': response['response'][0]['members_count']            
        }

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
        if 'error' in response:
            errors.append(f"it is not possible to get a list of groups from the user id {self.user_id}: {response['error']['error_msg']}")
        return set(response['response']['items'])
    
def main(token, user_id):
    '''
    the main algorithm of the problem
    '''

    user = User(token, user_id)

    result = user.groups_ids

    #steps_count = len(user.friends_ids)
   
    for friend_id in user.friends_ids:

        time.sleep(DELAY)
            
        friend = User(token, friend_id)

        try:
            friend_groups = friend.groups_ids
        except:
            continue
        finally:
            print('.', end='')            
            
        result -= friend_groups

    print('')

    'Putting the results in the files'
    data = []
    with open('output.json', 'w') as file:
        for foo in result:
            item = Group(token, foo)
            data.append(item.data)
        json.dump(data, file, ensure_ascii=False, indent=4)

    if len(errors) > 0:
        with open('errors.txt', 'w') as file:
            for error in errors:
                file.write(f'{error}\n')

    return result  
   

if __name__ == '__main__':

    input_id = input(f'Please enter user ID (Enter - {USER_ID}): ').strip()

    user_id = check_valid_user_id(TOKEN, input_id if input_id != '' else USER_ID)

    if user_id:
        groups_set = main(TOKEN, user_id)
    else:
        print(f'{input_id} is not valid user id. The program was interrupted.')

    if len(groups_set) >0:
        print(f'The list of groups in the VK that the user is in, but none of his friends are in, is displayed in the file output.txt')
    else:
        print('The user has no secrets from their friends :-)')
        
    if len(errors) > 0: print('Some of the user information was not processed, see the file errors.txt')

        

