import sources_vk
import unittest
import vk


class TestVkSources(unittest.TestCase):

    def test_retrieve_public_pages_from_vk(self):
        access_token = sources_vk.get_access_token()
        number_of_pages = 25
        search_queries = ['VK']
        output = sources_vk.get_vk_public_page_list(access_token, search_queries, 
                                                    results_per_query=number_of_pages)
        self.assertEqual(len(output), number_of_pages)
        for public_page in output:
            self.assertIsInstance(public_page, dict)

    def test_get_vk_public_page_id_set(self):
        known_input = [{"name": "page1", "gid": 97616552},
                       {"name": "страница2", "gid": 77157551},
                       {"name": "page3", "gid": 104610799, "somethingelse": 1}]
        expected_output = set([97616552, 104610799, 77157551])
        output = sources_vk.get_vk_public_page_id_set(known_input)
        self.assertEqual(output, expected_output)

    def test_retrieve_vk_posts(self):
        access_token = sources_vk.get_access_token()
        number_of_posts = 5
        tproger_page_id = 30666517
        result = sources_vk.get_last_vk_community_posts(access_token, tproger_page_id, 
                                                        count=number_of_posts)
        self.assertEqual(len(result), number_of_posts)
        for post in result:
            self.assertIsInstance(post, dict)

    def test_filter_lifeless_vk_pages(self):
        access_token = sources_vk.get_access_token()
        # one should check if the pages are still in live/dead state 
        # by visiting vk.com/club{id}
        known_input = {30666517, 101965347, 104116333}
        expected_output = {30666517, 101965347}
        filtering_rule = sources_vk.is_lifeless_vk_page
        output = sources_vk.filter_vk_pages(access_token, known_input, filtering_rule)
        self.assertEqual(output, expected_output)

    def test_filter_spam_vk_pages(self):
        access_token = sources_vk.get_access_token()
        # one should check if the pages are still not banned and stuff 
        # by visiting vk.com/club{id}
        known_input = {30666517, 101965347, 35583485, 103174736}
        expected_output = {30666517, 101965347}
        filtering_rule = sources_vk.is_spam_vk_page
        output = sources_vk.filter_vk_pages(access_token, known_input, filtering_rule)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
