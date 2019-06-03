
from tools import vk_request,users_search_on_age

res = vk_request('users.search','university=1088')
print(res)
users = users_search_on_age('university=1088')
print(len(users))