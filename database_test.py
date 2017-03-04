import unittest

import database

class TestPostDatabase(unittest.TestCase):
    # Note that database files are not getting deleted, but
    #   since they have similar names, it's not hard to do by hand.

    def test_inserting_and_loading_of_single_valid_post(self):
        db = database.PostDatabase('_test_post_db1')
        known_input = {'date': 1, 'summary': 'qweqwe', 'link': 'qweqwe'}
        expected_output = [known_input]
        db.insert_post_uniquely(known_input)
        output = db.load_posts()
        self.assertEqual(output, expected_output)
        db.erase_all_data()

    def test_inserting_post_with_missing_field(self):
        db = database.PostDatabase('_test_post_db2')
        known_input = {'summary': 'qweqwe', 'link': 'qweqwe'}
        with self.assertRaises(ValueError):
            db.insert_post_uniquely(known_input)
        db.erase_all_data()

    def test_inserting_post_with_unnecessary_field(self):
        db = database.PostDatabase('_test_post_db3')
        known_input = {'text': 'asd', 'date': 1, 'summary': 'qweqwe', 'link': 'qweqwe'}
        with self.assertRaises(ValueError):
            db.insert_post_uniquely(known_input)
        db.erase_all_data()

    def test_insert_uniquely_dublicate_posts(self):
        db = database.PostDatabase('_test_post_db4')
        post1 = {'date': 1, 'summary': 'qweqwe', 'link': 'post1'}
        post2 = {'date': 2, 'summary': 'qweqwe', 'link': 'post1'}
        post3 = {'date': 1, 'summary': 'qwe', 'link': 'post1'}
        expected_output = [post1]
        db.insert_post_uniquely(post1)
        db.insert_post_uniquely(post2)
        db.insert_post_uniquely(post3)
        output = db.load_posts()
        self.assertEqual(output, expected_output)
        db.erase_all_data()


    def test_insert_multiple_posts(self):
        db = database.PostDatabase('_test_post_db5')
        posts = [{'date': 1, 'summary': 'qweqwe', 'link': 'post1'},
                 {'date': 2, 'summary': 'qweqwe', 'link': 'post2'},
                 {'date': 1, 'summary': 'qwe', 'link': 'post3'},
                 ]
        db.insert_post_list_uniquely(posts)
        output = db.load_posts()
        self.assertEqual(len(output), len(posts))
        for post in posts:
            self.assertTrue(post in output)
        db.erase_all_data()


if __name__ == '__main__':
    unittest.main()
