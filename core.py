import tools as t

# res = t.vk_request('users.search','university=1088')
# print(res)
if (t.users_is_empty()):
    t.download_data_from_vk()
users = t.get_dict_for_graph()
graph = t.get_graph(users)
t.drow_graph(graph)
