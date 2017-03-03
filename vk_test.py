import vk
import unittest
import os

class TestVkRequest(unittest.TestCase):
    
    def test_make_api_request_without_access_token(self):
        output = vk.make_vk_api_request('users.get', user_ids=1, fields='screen_name')
        self.assertEqual(output['response'][0]['screen_name'], 'durov')

    def test_make_api_request_with_access_token(self):
        token = os.environ.get('VK_ACCESS_TOKEN')
        output = vk.make_vk_api_request('users.get', access_token=token)
        self.assertEqual(len(output['response']), 1)

    #def test_groups_search(self):
    #    access_token = os.environ('VK_ACCESS_TOKEN')
    #    print(groups_search(access_token, query='VK', type='page', count=10))


if __name__ == '__main__':
    unittest.main()
