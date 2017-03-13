import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../vk')))

import vk_posts
import vk_api

class TestVkPosts(unittest.TestCase):

    def test_retrieve_vk_posts_from_single_community(self):
        access_token = vk_api.get_access_token()
        number_of_posts = 5
        tproger_page_id = 30666517
        output = vk_posts.get_last_vk_community_posts(access_token, tproger_page_id, 
                                                      count=number_of_posts)
        self.assertEqual(len(output), number_of_posts)
        for post in output:
            self.assertIsInstance(post, dict)
    
    def test_retrieve_vk_posts_from_multiple_communities(self):
        access_token = vk_api.get_access_token()
        number_of_posts_per_community = 5
        page_ids = [30666517, 54530371]
        output = vk_posts.get_last_vk_posts_of_communities(access_token, page_ids,
                                                           number_of_posts_per_community)
        self.assertEqual(len(output), number_of_posts_per_community * len(page_ids))
        for post in output:
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

    def test_extract_post_text_summary_too_long_summary(self):
        known_input = ''.join(['1' for i in range(230)])
        expected_output = '%s...' % ''.join(['1' for i in range(100)])
        actual_output = vk_posts.extract_post_text_summary(known_input)
        self.assertEqual(actual_output, expected_output)

    def test_extract_post_text_summary_newline_break(self):
        long_string = ''.join(['1' for i in range(230)])
        known_input = '%s<br>%s' % (long_string[:63], long_string[63:])
        expected_output = ''.join(['1' for i in range(63)])
        actual_output = vk_posts.extract_post_text_summary(known_input)
        self.assertEqual(actual_output, expected_output)

    def test_extract_post_text_summary_space_break(self):
        long_string = ''.join(['1' for i in range(230)])
        known_input = '%s %s' % (long_string[:84], long_string[84:])
        expected_output = '%s...' % ''.join(['1' for i in range(84)])
        actual_output = vk_posts.extract_post_text_summary(known_input)
        self.assertEqual(actual_output, expected_output)

    def test_extract_post_text_summary_too_short_post_text(self):
        known_input = ''.join(['1' for i in range(5)])
        expected_output = known_input
        actual_output = vk_posts.extract_post_text_summary(known_input)
        self.assertEqual(actual_output, expected_output)

    def test_extract_post_text_summary_too_short_with_linebreak(self):
        known_input = 'Анализ со Stack Overflow средствами Python<br>#python #pirsipy'
        expected_output = 'Анализ со Stack Overflow средствами Python'
        actual_output = vk_posts.extract_post_text_summary(known_input)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
