import unittest
import tools
import psycopg2

class Test(unittest.TestCase):

    def test_user_search_on_mouth(self):
        res = tools.vk_request('users.search', f'age_from=21&age_to=22&university=1088')
        users = tools.users_search_on_mouth(21,'university=1088')
        self.assertEqual(res['response']['count'],len(users))

    def test_get_friends(self):
        users = tools.get_items(tools.vk_request('users.search', f'age_from=21&age_to=22&university=1088'))
        friends = tools.get_friends(users)
        self.assertIsNotNone(friends)

    def test_friends_write_to_db(self):
        tools.write_users_to_db([{'id':1, 'first_name': 'a', 'last_name': 'b'}])
        ids = list(range(0,1010))
        tools.write_friends_to_db({1:ids})
        conn = tools.get_coonnect()
        cur = conn.cursor()
        cur.execute('select count(*) from friends where interval_id < 1010')
        rows = cur.fetchall()
        self.assertEqual(rows[0][0],1010)
        cur.execute('delete from users where id=1')
        cur.execute('delete from friends where interval_id < 1010')
        conn.commit()
        cur.close()
        conn.close()

    def test_user_write_to_db(self):
        users = []
        for id in range(0, 1010):
            users.append({'id': id, 'first_name': 'a', 'last_name': 'b'})
        tools.write_users_to_db(users)
        conn = tools.get_coonnect()
        cursor = conn.cursor()
        cursor.execute('select count(*) from users where id<1010')
        rows = cursor.fetchall()
        self.assertEqual(1010,rows[0][0])
        cursor.execute('delete from users where id<1010')
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    unittest.main()