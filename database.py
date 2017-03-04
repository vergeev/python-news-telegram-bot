from os import remove

from tinydb import TinyDB, where

class PostDatabase:

    def __init__(self, filepath):
        self.db = TinyDB('%s.json' % filepath) 

    def load_posts(self):
        return self.db.all()
    
    def _raise_if_invalid_post(self, post):
        allowed_fields = ['date', 'summary', 'link']
        error_message = 'Only the following fields are allowed: %s' % str(allowed_fields)
        for allowed_field in allowed_fields:
            if allowed_field not in post.keys():
                raise ValueError(error_message)
        if len(allowed_fields) != len(post.keys()):
            raise ValueError(error_message)

    def _is_dublicate(self, post):
        return self.db.contains(where('link') == post['link'])

    def insert_post_uniquely(self, post):
        self._raise_if_invalid_post(post)
        if self._is_dublicate(post):
            return
        self.db.insert(post)

    def insert_post_list_uniquely(self, posts):
        for post in posts:
            self.insert_post_uniquely(post)

    def erase_all_data(self):
        self.db.purge()
