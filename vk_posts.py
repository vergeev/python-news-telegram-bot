import json
import os
from sys import stdin
from argparse import ArgumentParser, FileType

from database import PostDatabase
from vk import wall_get, invoke_with_cooldown, get_access_token


def get_last_vk_community_posts(access_token, community_id, count=10):
    owner_id = -1 * community_id  # indicate that this is a community
    post_list = invoke_with_cooldown(wall_get, access_token=access_token, 
                                     owner_id=owner_id, filter='owner', count=count)
    return post_list


def get_last_vk_posts_of_communities(access_token, community_ids, posts_per_community=10):
    posts = []
    for community_id in community_ids:
        posts += get_last_vk_community_posts(access_token, community_id, 
                                             posts_per_community)
    return posts


def is_python_post(post):
    keywords = ['python', 'django', 'flask']
    for keyword in keywords:
        if keyword.lower() in post['text'].lower():
            return True
    return False


def extract_post_text_summary(post_text):
    summary_length = 100

    first_newline_position = post_text[:summary_length].find('<br>') 
    if first_newline_position != -1:
        return post_text[:first_newline_position]

    if len(post_text) < summary_length:
        return post_text

    last_whitespace_position = post_text[:summary_length].rfind(' ')
    if last_whitespace_position != -1:
        return '%s...' % post_text[:last_whitespace_position]

    return '%s...' % post_text[:summary_length]


def form_vk_post_link(page_id, post_id):
    return "https://vk.com/wall%d_%d" % (page_id, post_id)


def strip_irrelevant_post_info(raw_post):
    return {'date': raw_post['date'],
            'summary': extract_post_text_summary(raw_post['text']),
            'link': form_vk_post_link(raw_post['from_id'], raw_post['id']),
            }


def strip_vk_posts(post_list):
    return [strip_irrelevant_post_info(post) for post in post_list]


def store_to_database(post_list, database_name):
    db = PostDatabase(database_name)
    db.insert_post_list_uniquely(post_list)


def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument('-i', '--infile', type=FileType('r'), default=stdin,
                        help='JSON file with vk source page ids')
    parser.add_argument('-o', '--outfile', type=str, default='posts.json', 
                        help='the name of database where posts will be stored')
    return parser


if __name__ == '__main__':
    args = get_argument_parser().parse_args()
    page_ids = json.load(args.infile)
    access_token = get_access_token()
    print('Getting the news...')
    posts = get_last_vk_posts_of_communities(access_token, page_ids)
    print('Filtering the news...')
    python_posts = list(filter(is_python_post, posts))
    python_not_suggested_posts = list(filter(lambda p: 'signer_id' not in p, python_posts))
    python_stripped_not_suggested_posts = strip_vk_posts(python_not_suggested_posts) 
    print('Storing the news...')
    store_to_database(python_stripped_not_suggested_posts, args.outfile)
    print('Done.')
