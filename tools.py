import urllib.request, json
from my_token import token

def vk_request(method,params):
    url = "https://api.vk.com/method/"+ method + "?"+ params +"&access_token=" + token + "&v=5.92"
    response = urllib.request.urlopen(url)
    return json.loads(response.read().decode('utf8'))

def get_items(json_object):
    if ('response' in json_object) :
        return json_object['response']['items']
    else:
        return None


