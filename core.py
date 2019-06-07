import tools

res = tools.vk_request('users.search','university=1088')
print(res)
if (tools.users_is_empty()):
    users = tools.users_search_on_age('university=1088')
    friends = tools.get_friends(users)
    tools.write_users_to_db(users)
    tools.write_friends_to_db(friends)

print(len(users))
print(len(users))

