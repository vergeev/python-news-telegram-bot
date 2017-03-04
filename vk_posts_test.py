import unittest
from os import remove

import vk_posts
from vk import get_access_token

class TestVkPosts(unittest.TestCase):

    def test_retrieve_vk_posts(self):
        access_token = get_access_token()
        number_of_posts = 5
        tproger_page_id = 30666517
        result = vk_posts.get_last_vk_community_posts(access_token, tproger_page_id, 
                                                      count=number_of_posts)
        self.assertEqual(len(result), number_of_posts)
        for post in result:
            self.assertIsInstance(post, dict)

    def test_form_vk_post_link(self):
        page_id = -30666517
        post_id = 1472604
        expected_output = 'https://vk.com/wall-30666517_1472604'
        output = vk_posts.form_vk_post_link(page_id, post_id)
        self.assertEqual(output, expected_output)

    def test_strip_vk_posts(self):
        relevant_fields = ['date', 'summary', 'link']
        known_input = [{'date': 1, 'id': 1,
                        'text': 'qwe', 'from_id': 1},
                       {'irrelevant_field': 1, 'date': 1,
                        'text': 'qwe', 'from_id': 1, 'id': 1},
                       ]
        output = vk_posts.strip_vk_posts(known_input)
        for post in output:
            self.assertEqual(post.get('irrelevant_field'), None)
            for field in relevant_fields:
                self.assertNotEqual(post[field], None)


if __name__ == '__main__':
    unittest.main()
