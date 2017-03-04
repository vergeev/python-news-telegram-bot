import unittest
from os import remove

import vk_posts
from vk import get_access_token

class TestVkPosts(unittest.TestCase):

    def test_retrieve_vk_posts_from_single_community(self):
        access_token = get_access_token()
        number_of_posts = 5
        tproger_page_id = 30666517
        output = vk_posts.get_last_vk_community_posts(access_token, tproger_page_id, 
                                                      count=number_of_posts)
        self.assertEqual(len(output), number_of_posts)
        for post in output:
            self.assertIsInstance(post, dict)
    
    def test_retrieve_vk_posts_from_multiple_communities(self):
        access_token = get_access_token()
        number_of_posts_per_community = 5
        page_ids = [30666517, 54530371]
        output = vk_posts.get_last_vk_posts_of_communities(access_token, page_ids,
                                                           number_of_posts_per_community)
        self.assertEqual(len(output), number_of_posts_per_community * len(page_ids))
        for post in output:
            self.assertIsInstance(post, dict)

    def test_get_python_posts(self):
        known_input = [{'text': 'Подборка по Python на все случаи жизни! Хотите?'},
                       {'text': 'Что-то про Flask'},
                       {'text': 'Что-то про dJaNgO'},
                       {'text': 'Практика в open-source проектах часто помогает...'},
                       ]
        expected_output = [{'text': 'Подборка по Python на все случаи жизни! Хотите?'},
                           {'text': 'Что-то про Flask'},
                           {'text': 'Что-то про dJaNgO'},
                           ]
        output = vk_posts.get_good_posts(known_input, vk_posts.is_python_post)
        self.assertEqual(len(output), len(expected_output))
        for post in expected_output:
            self.assertTrue(post in output, post['text'])

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
