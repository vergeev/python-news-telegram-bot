import os
import time
import getpass
import argparse
import sys
import vk
import json


def try_to_fetch_existing_session():
    token = os.environ.get('VK_ACCESS_TOKEN')
    if token is None:
        return None
    return vk.AuthSession(access_token=token)


def ask_for_password_and_get_session():
    app_id = os.environ['VK_API_APP_ID']
    login = input('VK login: ')
    password = getpass.getpass('Password: ')
    #FIXME: save access token to environ
    return vk.AuthSession(user_login=login, user_password=password, app_id=app_id)


def get_vk_public_page_list(vk_api, search_queries, results_per_query=20):
    public_pages = []
    for query in search_queries:
        search_res = vk_api.groups.search(q=query, type='page', count=results_per_query)
        public_pages += search_res[1:]
    return public_pages


def get_vk_public_page_id_set(public_page_list):
    return {page['gid'] for page in public_page_list}


def get_last_vk_community_posts(vk_api, community_id, count=10):
    # for additional info, see https://vk.com/dev/wall.get
    owner_id = -1 * community_id  # indicate that this is a community
    posts = vk_api.wall.get(owner_id=owner_id, filter='owner', count=count)
    return posts[1:]


def is_less_than_day(seconds):
    return seconds < 24 * 60 * 60


def select_latest_post(vk_post_list):
    return max(vk_post_list, key=lambda p: p['date'])


def is_lifeless_vk_page(vk_api, page_id):
    number_of_posts_to_test = 5
    posts = get_last_vk_community_posts(vk_api, page_id, count=number_of_posts_to_test)
    latest_post_time_difference = time.time() - select_latest_post(posts)['date']
    if not is_less_than_day(latest_post_time_difference):
        return True
    for index, post in enumerate(posts[2:]):
        time_difference = posts[index - 1]['date'] - post['date']
        if not is_less_than_day(time_difference):
            return True
    return False


def is_spam_vk_page(vk_api, page_id):
    page = vk_api.groups.getById(group_id=page_id, fields='description')[0]
    stop_words = ['курсов', 'помощь', 'на заказ']
    for stop_word in stop_words:
        if stop_word.lower() in page['name'].lower():
            return True
        if stop_word.lower() in page['description'].lower():
            return True
    return False


def filter_vk_pages(vk_api, page_id_set, is_bad_page_id):
    good_vk_page_ids = set()
    for page_id in page_id_set:
        if is_bad_page_id(vk_api, page_id):
            continue
        good_vk_page_ids.add(page_id)
    return good_vk_page_ids
    

def save_data(data, outfile):
    json.dump(data, outfile)


#FIXME: move get_striped_vk_posts to the appropriate module
def form_vk_post_link(page_id, post_id):
    return "https://vk.com/wall%d_%d" % (page_id, post_id)


def strip_irrelevant_post_info(raw_post):
    return {'date': raw_post['date'],
            'text': raw_post['text'],
            'link': form_vk_post_link(raw_post['from_id'], raw_post['id']),
            }


def get_stripped_vk_posts(post_list):
    return [strip_irrelevant_post_info(post) for post in post_list]


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'), default=sys.stdout)
    return parser


if __name__ == '__main__':
    args = get_argument_parser().parse_args()
    search_queries = ['программист', 'программирование', 'Python']
    session = try_to_fetch_existing_session() or ask_for_password_and_get_session()
    api = vk.API(session)
    pages = get_vk_public_page_list(api, search_queries)
    page_ids = get_vk_public_page_id_set(pages)
    page_ids = filter_vk_pages(api, page_ids, is_lifeless_vk_page)
    page_ids = filter_vk_pages(api, page_ids, is_spam_vk_page)
    save_data(page_ids, outfile)
