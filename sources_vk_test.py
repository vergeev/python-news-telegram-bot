import sources_vk
import unittest
import vk


class TestVkSources(unittest.TestCase):

    def get_vk_api(self):
        session = sources_vk.try_to_fetch_existing_session()
        session = session or sources_vk.ask_for_password_and_get_session()
        return vk.API(session)
        
    def test_retrieve_public_pages_from_vk(self):
        api = self.get_vk_api()
        number_of_pages = 25
        search_queries = ['VK']
        output = sources_vk.get_vk_public_page_list(api, search_queries, 
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
        api = self.get_vk_api()
        number_of_posts = 5
        tproger_page_id = 30666517
        result = sources_vk.get_last_vk_community_posts(api, tproger_page_id, 
                                                       count=number_of_posts)
        self.assertEqual(len(result), number_of_posts)
        for post in result:
            self.assertIsInstance(post, dict)

    def test_form_vk_post_link(self):
        page_id = -30666517
        post_id = 1472604
        expected_output = 'https://vk.com/wall-30666517_1472604'
        output = sources_vk.form_vk_post_link(page_id, post_id)
        self.assertEqual(output, expected_output)

    def test_get_stripped_vk_posts(self):
        relevant_fields = ['date', 'text', 'link']
        known_input = [{'date': 1, 'id': 1,
                        'text': 'qwe', 'from_id': 1},
                       {'irrelevant_field': 1, 'date': 1,
                        'text': 'qwe', 'from_id': 1, 'id': 1},
                       ]
        output = sources_vk.get_stripped_vk_posts(known_input)
        for post in output:
            self.assertEqual(post.get('irrelevant_field'), None)
            for field in relevant_fields:
                self.assertNotEqual(post[field], None)

    def test_filter_lifeless_vk_pages(self):
        api = self.get_vk_api()
        # one should check if the pages are still in live/dead state 
        # by visiting vk.com/club{id}
        known_input = {30666517, 101965347, 104116333}
        expected_output = {30666517, 101965347}
        filtering_rule = sources_vk.is_lifeless_vk_page
        output = sources_vk.filter_vk_pages(api, known_input, filtering_rule)
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
