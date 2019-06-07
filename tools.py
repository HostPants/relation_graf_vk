import urllib.request, json
import time
from my_token import token
import psycopg2

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
    for age in range(10, 20):
        res = vk_request('users.search', f'age_from={age}&age_to={age + 1}&{params}&count=1000')
        time.sleep(1 / 3)
        # if res['response']['count'] > 1000:
        #     users += users_search_on_mouth(age, params)
        # else:
        users += get_items(res)
    return users

def users_search_on_mouth(age, params):
    users = []
    for mouth in range(1, 13):
        res = vk_request('users.search', f'age_from={age}&age_to={age + 1}&birth_month={mouth}&{params}&count=1000')
        time.sleep(1 / 3)
        users += get_items(res)
    return users

def get_friends(users):
    friends = {}
    for user in users:
        items = get_items(vk_request('friends.get', f"user_id={user['id']}"))
        time.sleep(1/3)
        friends[user['id']] = items
    return friends

def get_coonnect():
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        database='vk_graf',
        user='vk',
        password='pass100word')
    return conn

def users_is_empty():
    conn = get_coonnect()
    cur = conn.cursor()
    cur.execute('select count(*) from users')
    count = cur.fetchall()
    if count[0][0] > 0:
        return False
    else:
        return True

def write_users_to_db(users):
    conn = get_coonnect()
    cursor = conn.cursor()
    values= 'values'
    ids = set()
    for user in users:
        id = user['id']
        first_name = user['first_name']
        last_name = user['last_name']
        if id not in ids:
            values += f" ('{id}', '{first_name}', '{last_name}'),"
            ids.add(id)
            if len(ids) % 1000 == 0:
                cursor.execute('insert into users ' + values[:-1])
                values='values'
    cursor.execute('insert into users ' + values[:-1])
    conn.commit()
    cursor.close()
    conn.close()



def write_friends_to_db(friends):
    conn = get_coonnect()
    cursor = conn.cursor()
    values = 'values'
    id=0;
    for user_id,friends_ids in friends.items():
        count =0;
        for friend_id in set(friends_ids):
            values += f" ('{id}', '{friend_id}'),"
            count+=1;
            if count % 1000 == 0 or len(friends_ids) == count:
                cursor.execute(f"insert into friends(interval_id,friends_id){values[:-1]}")
                cursor.execute(f"insert into users_together_friends (user_id,friends_ids,amount) values({user_id},{id},{len(friends_ids)})")
                values = 'values'
            id += 1;
    conn.commit()
    cursor.close()
    conn.close()