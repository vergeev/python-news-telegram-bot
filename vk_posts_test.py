import vk_posts
import unittest

class TestVkPosts(unittest.TestCase):

    def test_form_vk_post_link(self):
        page_id = -30666517
        post_id = 1472604
        expected_output = 'https://vk.com/wall-30666517_1472604'
        output = vk_posts.form_vk_post_link(page_id, post_id)
        self.assertEqual(output, expected_output)

    def test_strip_vk_posts(self):
        relevant_fields = ['date', 'text', 'link']
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
