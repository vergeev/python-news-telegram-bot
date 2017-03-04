import json
import sys
import argparse
from os import remove

from database import PostDatabase

def load_vk_source_ids_set(source_file):
    return set(json.load(source_file))


def get_vk_posts(source_vk_ids):
    raise NotImplemented


def is_python_post(post):
    raise NotImplemented


def filter_posts(post_list, is_good_post):
    raise NotImplemented


def form_vk_post_link(page_id, post_id):
    return "https://vk.com/wall%d_%d" % (page_id, post_id)


def strip_irrelevant_post_info(raw_post):
    return {'date': raw_post['date'],
            'text': raw_post['text'],
            'link': form_vk_post_link(raw_post['from_id'], raw_post['id']),
            }


def strip_vk_posts(post_list):
    return [strip_irrelevant_post_info(post) for post in post_list]


def store_to_database(post_list, database_name):
    db = PostDatabase(database_name)
    db.insert_post_list_uniquely(post_list)


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', type=argparse.FileType('r'), default=sys.stdin,
                        help='JSON file with vk source page ids')
    parser.add_argument('-o', '--outfile', type=str, default='posts', 
                        help='the name of database where posts will be stored')


if __name__ == '__main__':
    args = get_argument_parser()
    source_ids = load_vk_source_ids_set(args.infile)
    posts = get_vk_posts(source_ids)
    python_posts = filter_posts(posts, is_python_post)
    python_stripped_posts = strip_vk_posts(python_posts)
    store_to_database(python_stripped_posts, args.outfile)
