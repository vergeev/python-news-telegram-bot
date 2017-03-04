import json
import sys
import argparse
from os import remove

def form_vk_post_link(page_id, post_id):
    return "https://vk.com/wall%d_%d" % (page_id, post_id)


def strip_irrelevant_post_info(raw_post):
    return {'date': raw_post['date'],
            'text': raw_post['text'],
            'link': form_vk_post_link(raw_post['from_id'], raw_post['id']),
            }


def strip_vk_posts(post_list):
    return [strip_irrelevant_post_info(post) for post in post_list]


def load_source_ids_set(source_file):
    return set(json.load(source_file))


def load_existing_posts(posts_file):
    raise NotImplemented


def save_posts(posts, filename):
    raise NotImplemented


def save_with_existing_posts(posts, filename):
    raise NotImplemented


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', type=argparse.FileType('r'), default=sys.stdin,
                        help='JSON file with vk source page ids')
    parser.add_argument('-o', '--outfile', type=str, default='posts.json', 
                        help='JSON file where posts will be stored')


if __name__ == '__main__':
    args = get_argument_parser()
    source_ids = load_source_ids_set(args.infile)
    posts = get_vk_posts(source_ids)
    python_posts = filter_posts(posts, is_python_post)
    python_stripped_posts = strip_vk_posts(python_posts)
    save_with_existing_posts(python_stripped_posts, args.outfile)
