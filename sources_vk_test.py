import sources_vk
import unittest
import vk


class TestVkSources(unittest.TestCase):

    def test_retrieve_default_number_of_pages_from_vk(self):
        default_number_of_pages = 20
        search_queries = ['VK']
        session = sources_vk.try_to_fetch_existing_session()
        session = session or sources_vk.ask_for_password_and_get_session()
        api = vk.API(session)
        result = sources_vk.get_vk_public_page_list(api, search_queries)
        self.assertEqual(len(result), default_number_of_pages)
        for public_page in result:
            self.assertIsInstance(public_page, dict)

    def test_get_vk_public_page_id_set(self):
        known_input = [{"name": "page1", "gid": 97616552},
                       {"name": "страница2", "gid": 77157551},
                       {"name": "page3", "gid": 104610799, "somethingelse": 1}]
        known_output = set([97616552, 104610799, 77157551])
        output = sources_vk.get_vk_public_page_id_set(known_input)
        self.assertEqual(output, known_output)


if __name__ == '__main__':
    unittest.main()
