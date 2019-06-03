import unittest
import tools

class Test(unittest.TestCase):

    def test_user_search_on_mouth(self):
        res = tools.vk_request('users.search', f'age_from=20&age_to=21&university=1088')
        users = tools.users_search_on_mouth(20,'university=1088')
        self.assertEqual(res['response']['count'],len(users))

    def test_user_search_on_age(self):
        res = tools.vk_request('users.search', 'university=1088')
        users = tools.users_search_on_age('university=1088')
        self.assertEqual(res['response']['count'],len(users))

if __name__ == '__main__':
    unittest.main()