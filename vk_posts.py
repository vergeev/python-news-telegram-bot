import json
import os
import html
import sys
import argparse

import tinydb

import vk_api


def get_last_vk_community_posts(access_token, community_id, count=10):
    owner_id = -1 * community_id  # indicate that this is a community
    post_list = vk_api.invoke_with_cooldown(vk_api.wall_get, access_token=access_token, 
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


def is_not_suggested_post(post):
    return 'signer_id' not in post


def is_not_ads_post(post):
    return not post['marked_as_ads']


def filter_raw_python_posts(raw_posts):
    almost_filtered_posts = list(filter(is_python_post, raw_posts))
    almost_filtered_posts = list(filter(is_not_suggested_post, almost_filtered_posts))
    filtered_posts = list(filter(is_not_ads_post, almost_filtered_posts))
    return filtered_posts


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
            'summary': html.unescape(extract_post_text_summary(raw_post['text'])),
            'link': form_vk_post_link(raw_post['from_id'], raw_post['id']),
            }


def strip_vk_posts(post_list):
    return [strip_irrelevant_post_info(post) for post in post_list]


def is_dublicate(post, database):
    return database.contains(tinydb.where('link') == post['link'])


def store_posts_to_database(posts, database):
    for post in posts:
        if is_dublicate(post, database):
            continue
        database.insert(post)


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', type=argparse.FileType('r'), 
                        default='sources.json',
                        help='JSON file with vk source page ids')
    parser.add_argument('-o', '--outfile', type=str, default='posts.json', 
                        help='the name of database where posts will be stored')
    return parser


if __name__ == '__main__':
    args = get_argument_parser().parse_args()
    page_ids = json.load(args.infile)
    access_token = vk_api.get_access_token()
    if access_token is None:
        print('No access token was received. Try running installation_guide.py.')
        sys.exit()
    print('Getting the news...')
    posts = get_last_vk_posts_of_communities(access_token, page_ids)
    print('Filtering the news...')
    filtered_posts = filter_raw_python_posts(posts)
    stripped_filtered_posts = strip_vk_posts(filtered_posts) 
    print('Storing the news...')
    database = tinydb.TinyDB(args.outfile)
    store_posts_to_database(stripped_filtered_posts, database)
    print('Done.')
