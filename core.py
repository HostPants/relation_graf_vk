import tools

res = tools.vk_request('users.search','university=1088')
print(res)
if (tools.users_is_empty()):
    tools.download_data_from_vk()
