import os
import time
import getpass
import argparse
import sys
import json

import vk_api
import vk_posts


def get_vk_public_page_list(access_token, search_queries, results_per_query=20):
    public_pages = []
    for query in search_queries:
        public_pages += vk_api.groups_search(access_token, query=query, type='page', 
                                             count=results_per_query)
    return public_pages


def is_less_than_day(seconds):
    return seconds < 24 * 60 * 60


def select_latest_post(vk_post_list):
    return max(vk_post_list, key=lambda p: p['date'])


def is_vk_page_alive(access_token, page_id):
    number_of_posts_to_test = 5
    posts = vk_posts.get_last_vk_community_posts(access_token, page_id, 
                                                 count=number_of_posts_to_test)
    latest_post_time_difference = time.time() - select_latest_post(posts)['date']
    if not is_less_than_day(latest_post_time_difference):
        return False
    for index, post in enumerate(posts[2:]):
        time_difference = posts[index - 1]['date'] - post['date']
        if not is_less_than_day(time_difference):
            return False
    return True


def get_group_by_id_with_description(access_token, group_id):
    group_get_by_id = vk_api.group_get_by_id
    return vk_api.invoke_with_cooldown(group_get_by_id, access_token=access_token, 
                                       group_id=group_id, fields='description')[0]


def is_vk_page_not_spam(access_token, page_id):
    page = get_group_by_id_with_description(access_token, page_id)
    stop_words = ['курсов', 'помощь', 'на заказ']
    for stop_word in stop_words:
        if stop_word.lower() in page['name'].lower():
            return False
        if stop_word.lower() in page['description'].lower():
            return False
    return True


def filter_vk_pages(access_token, page_id_list, is_bad_page_id):
    return list(filter(lambda page: is_bad_page_id(access_token, page), page_id_list))


def save_data(data, outfile):
    json.dump(data, outfile)


def get_access_token():
    return os.environ.get('VK_ACCESS_TOKEN')


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'), default=sys.stdout)
    return parser


if __name__ == '__main__':
    args = get_argument_parser().parse_args()
    access_token = vk_api.get_access_token()
    if access_token is None:
        print('No access token. Try running installation_guide.py.')
        sys.exit()
    search_queries = ['программист', 'программирование', 'Python']
    print('Getting the public pages...')
    pages = get_vk_public_page_list(access_token, search_queries)
    page_ids = [page['gid'] for page in pages]
    print('Filtering dead public pages...')
    page_ids = filter_vk_pages(access_token, page_ids, is_vk_page_alive)
    print('Filtering spam public pages...')
    page_ids = filter_vk_pages(access_token, page_ids, is_vk_page_not_spam)
    print('Saving page ids...')
    save_data(list(page_ids), args.outfile)
    print('Done.')
