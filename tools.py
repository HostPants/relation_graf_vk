import urllib.request, json
import time
from my_token import token

def vk_request(method,params):
    url = f"https://api.vk.com/method/{method}?{params}&access_token={token}&v=5.92"
    response = urllib.request.urlopen(url)
    return json.loads(response.read().decode('utf8'))

def get_items(json_object):
    if ('response' in json_object) :
        return json_object['response']['items']
    else:
        return None

def users_search_on_age(params):
    users = []
    for age in range(10, 100):
        res = vk_request('users.search', f'age_from={age}&age_to={age + 1}&{params}&count=1000')
        time.sleep(1 / 3)
        if res['response']['count'] > 1000:
           users += users_search_on_mouth(age, params)
        else:
            users += get_items(res)
    return users

def users_search_on_mouth(age, params):
    users = []
    for mouth in range(1, 13):
        res = vk_request('users.search', f'age_from={age}&age_to={age + 1}&birth_month={mouth}&{params}&count=1000')
        time.sleep(1 / 3)
        users += get_items(res)
    return users
