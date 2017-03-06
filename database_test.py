import unittest
import os

import database

class TestPostDatabase(unittest.TestCase):

    def test_inserting_and_loading_of_single_valid_post(self):
        db_name = '_test_post_db1'
        db = database.PostDatabase(db_name)
        known_input = {'date': 1, 'summary': 'qweqwe', 'link': 'qweqwe'}
        expected_output = [known_input]
        db.insert_post_uniquely(known_input)
        output = db.load_posts()
        self.assertEqual(output, expected_output)
        os.remove(db_name)

    def test_inserting_post_with_missing_field(self):
        db_name = '_test_post_db2'
        db = database.PostDatabase(db_name)
        known_input = {'summary': 'qweqwe', 'link': 'qweqwe'}
        with self.assertRaises(ValueError):
            db.insert_post_uniquely(known_input)
        os.remove(db_name)

    def test_inserting_post_with_unnecessary_field(self):
        db_name = '_test_post_db3'
        db = database.PostDatabase(db_name)
        known_input = {'text': 'asd', 'date': 1, 'summary': 'qweqwe', 'link': 'qweqwe'}
        with self.assertRaises(ValueError):
            db.insert_post_uniquely(known_input)
        os.remove(db_name)

    def test_insert_uniquely_dublicate_posts(self):
        db_name = '_test_post_db4'
        db = database.PostDatabase(db_name)
        post1 = {'date': 1, 'summary': 'qweqwe', 'link': 'post1'}
        post2 = {'date': 2, 'summary': 'qweqwe', 'link': 'post1'}
        post3 = {'date': 1, 'summary': 'qwe', 'link': 'post1'}
        expected_output = [post1]
        db.insert_post_uniquely(post1)
        db.insert_post_uniquely(post2)
        db.insert_post_uniquely(post3)
        output = db.load_posts()
        self.assertEqual(output, expected_output)
        os.remove(db_name)

    def test_insert_multiple_posts(self):
        db_name = '_test_post_db5'
        db = database.PostDatabase(db_name)
        posts = [{'date': 1, 'summary': 'qweqwe', 'link': 'post1'},
                 {'date': 2, 'summary': 'qweqwe', 'link': 'post2'},
                 {'date': 1, 'summary': 'qwe', 'link': 'post3'},
                 ]
        db.insert_post_list_uniquely(posts)
        output = db.load_posts()
        self.assertEqual(len(output), len(posts))
        for post in posts:
            self.assertTrue(post in output)
        os.remove(db_name)

    def test_load_first_post_by_id(self):
        db_name = '_test_post_db6'
        db = database.PostDatabase(db_name)
        posts = [{'date': 1, 'summary': 'qweqwe', 'link': 'post1'},
                 {'date': 2, 'summary': 'qweqwe', 'link': 'post2'},
                 {'date': 1, 'summary': 'qwe', 'link': 'post3'},
                 ]
        db.insert_post_list_uniquely(posts)
        output = db.load_post_by_database_id(1)
        self.assertTrue(output == posts[0] or output == posts[1] or output == posts[2])
        os.remove(db_name)

    def test_getting_size(self):
        db_name = '_test_post_db7'
        db = database.PostDatabase(db_name)
        self.assertEqual(0, db.size())
        posts = [{'date': 1, 'summary': 'qweqwe', 'link': 'post1'},
                 {'date': 2, 'summary': 'qweqwe', 'link': 'post2'},
                 {'date': 1, 'summary': 'qwe', 'link': 'post3'},
                 ]
        db.insert_post_list_uniquely(posts)
        self.assertEqual(3, db.size())
        os.remove(db_name)

if __name__ == '__main__':
    unittest.main()
