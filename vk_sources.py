import os
import time
import getpass
import argparse
import sys
import json

import vk
from vk_posts import get_last_vk_community_posts


def get_vk_public_page_list(access_token, search_queries, results_per_query=20):
    public_pages = []
    for query in search_queries:
        public_pages += vk.groups_search(access_token, query=query, type='page', 
                                         count=results_per_query)
    return public_pages


def get_vk_public_page_id_set(public_page_list):
    return {page['gid'] for page in public_page_list}


def is_less_than_day(seconds):
    return seconds < 24 * 60 * 60


def select_latest_post(vk_post_list):
    return max(vk_post_list, key=lambda p: p['date'])


def is_lifeless_vk_page(access_token, page_id):
    number_of_posts_to_test = 5
    posts = get_last_vk_community_posts(access_token, page_id, 
                                        count=number_of_posts_to_test)
    latest_post_time_difference = time.time() - select_latest_post(posts)['date']
    if not is_less_than_day(latest_post_time_difference):
        return True
    for index, post in enumerate(posts[2:]):
        time_difference = posts[index - 1]['date'] - post['date']
        if not is_less_than_day(time_difference):
            return True
    return False


def get_group_by_id_with_description(access_token, group_id):
    group_get_by_id = vk.group_get_by_id
    return vk.invoke_with_cooldown(group_get_by_id, access_token=access_token, 
                                   group_id=group_id, fields='description')[0]


def is_spam_vk_page(access_token, page_id):
    page = get_group_by_id_with_description(access_token, page_id)
    stop_words = ['курсов', 'помощь', 'на заказ']
    for stop_word in stop_words:
        if stop_word.lower() in page['name'].lower():
            return True
        if stop_word.lower() in page['description'].lower():
            return True
    return False


def filter_vk_pages(access_token, page_id_set, is_bad_page_id):
    good_vk_page_ids = set()
    for page_id in page_id_set:
        if is_bad_page_id(access_token, page_id):
            continue
        good_vk_page_ids.add(page_id)
    return good_vk_page_ids
    

def save_data(data, outfile):
    json.dump(data, outfile)


def get_access_token():
    return os.environ.get('VK_ACCESS_TOKEN')


def print_no_access_token_error():
    print('No access token in VK_ACCESS_TOKEN environment variable.')
    print('Please see README.md on how to get it.')


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'), default=sys.stdout)
    return parser


if __name__ == '__main__':
    args = get_argument_parser().parse_args()
    access_token = vk.get_access_token()
    if access_token is None:
        print_no_access_token_error()
        sys.exit()
    search_queries = ['программист', 'программирование', 'Python']
    print('Getting the public pages...')
    pages = get_vk_public_page_list(access_token, search_queries)
    page_ids = get_vk_public_page_id_set(pages)
    print('Filtering dead public pages...')
    page_ids = filter_vk_pages(access_token, page_ids, is_lifeless_vk_page)
    print('Filtering spam public pages...')
    page_ids = filter_vk_pages(access_token, page_ids, is_spam_vk_page)
    print('Saving page ids...')
    save_data(list(page_ids), args.outfile)
    print('Done.')
