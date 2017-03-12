import vk_sources
import unittest

import vk


class TestVkSources(unittest.TestCase):

    def test_retrieve_public_pages_from_vk(self):
        access_token = vk.get_access_token()
        number_of_pages = 25
        search_queries = ['VK']
        output = vk_sources.get_vk_public_page_list(access_token, search_queries, 
                                                        results_per_query=number_of_pages)
        self.assertEqual(len(output), number_of_pages)
        for public_page in output:
            self.assertIsInstance(public_page, dict)

    def test_filter_lifeless_vk_pages(self):
        access_token = vk_sources.get_access_token()
        # one should check if the pages are still in live/dead state 
        # by visiting vk.com/club{id}
        known_input = [30666517, 101965347, 104116333]
        expected_output = [30666517, 101965347]
        filtering_rule = vk_sources.is_lifeless_vk_page
        output = vk_sources.filter_vk_pages(access_token, known_input, filtering_rule)
        self.assertEqual(output, expected_output)

    def test_filter_spam_vk_pages(self):
        access_token = vk_sources.get_access_token()
        # one should check if the pages are still not banned and stuff 
        # by visiting vk.com/club{id}
        known_input = [30666517, 101965347, 35583485, 103174736]
        expected_output = [30666517, 101965347]
        filtering_rule = vk_sources.is_spam_vk_page
        output = vk_sources.filter_vk_pages(access_token, known_input, filtering_rule)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
