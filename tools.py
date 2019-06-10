import urllib.request, json
import time
import networkx as nx
import psycopg2
from datetime import datetime
import matplotlib.pyplot as plt
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

def clear_users(users,ids):
    c_users = []
    for user in users:
        id = user['id']
        if id not in ids:
            c_users.append(user)

    return c_users;

def transform_name(name):
    return name.replace("'","''")

def download_data_from_vk():
    ids = set();
    for age in range(10, 21):
        res = vk_request('users.search', f'age_from={age}&age_to={age + 1}&university=1088&count=1000')
        time.sleep(1 / 3)

        # if res['response']['count'] > e:
        #     users += users_search_on_mouth(age, params)
        # else:
        users = get_items(res)
        users = clear_users(users,ids)
        ids.update(write_users_to_db(users))
        print('write to db next users: ',users)
        friends = get_friends(users)
        write_friends_to_db(friends)
        print('write to db next friends: ',friends)


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
            values += f" ('{id}', '{transform_name(first_name)}', '{transform_name(last_name)}'),"
            ids.add(id)
            if len(ids) % 1000 == 0 or len(ids) == len(users):
                cursor.execute('insert into users ' + values[:-1])
                values='values'
    conn.commit()
    cursor.close()
    conn.close()
    return ids;



def write_friends_to_db(friends):
    conn = get_coonnect()
    cursor = conn.cursor()
    values = 'values'
    for user_id,friends_ids in friends.items():
        if friends_ids is None:
            continue
        else:
            count = 0
        for friend_id in set(friends_ids):
            values += f" ( {user_id}, {friend_id}),"
            count+=1;
            if count % 1000 == 0 or len(friends_ids) == count:
                cursor.execute(f"insert into friends(user_id,friend_id){values[:-1]}")
                values = 'values'
    conn.commit()
    cursor.close()
    conn.close()

def get_dict_for_graph():
    conn = get_coonnect()
    cur = conn.cursor()
    cur.execute(f'select user_id, friend_id from friends join users on users.id = friends.friend_id')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    users = {}
    for row in rows:
        user_id = row[0]
        if  user_id not in users:
            users.update({user_id:[item[1] for item in rows if user_id == item[0]]})
    return users

def get_graph(users):
    return nx.from_dict_of_lists(users)

def drow_graph(graph):
    plt.figure(figsize=(10,10), dpi=200 )
    nx.draw(graph, node_size=5)
    plt.savefig("%s graph.png" % datetime.now().strftime('%H:%M:%S %d-%m-%Y'))
