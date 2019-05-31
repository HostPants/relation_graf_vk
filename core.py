import time
from tools import vk_request,get_items

res = vk_request('users.search','q=B&university=1088&count=20')
print(res)


