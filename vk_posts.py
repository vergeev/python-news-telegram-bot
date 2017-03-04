import json
import os
from sys import stdin
from argparse import ArgumentParser, FileType

from database import PostDatabase
from vk import wall_get, invoke_with_cooldown, get_access_token


def load_vk_source_ids_set(source_file):
    return set(json.load(source_file))


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


def get_good_posts(post_list, is_good_post):
    good_posts = []
    for post in post_list:
        if is_good_post(post):
            good_posts.append(post)
    return good_posts


def form_vk_post_link(page_id, post_id):
    return "https://vk.com/wall%d_%d" % (page_id, post_id)


def strip_irrelevant_post_info(raw_post):
    return {'date': raw_post['date'],
            'summary': raw_post['text'],  #FIXME: actually summarize the post
            'link': form_vk_post_link(raw_post['from_id'], raw_post['id']),
            }


def strip_vk_posts(post_list):
    return [strip_irrelevant_post_info(post) for post in post_list]


def store_to_database(post_list, database_name):
    db = PostDatabase(database_name)
    db.insert_post_list_uniquely(post_list)


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', type=argparse.FileType('r'), default=stdin,
                        help='JSON file with vk source page ids')
    parser.add_argument('-o', '--outfile', type=str, default='posts', 
                        help='the name of database where posts will be stored')


if __name__ == '__main__':
    args = get_argument_parser()
    page_ids = load_vk_source_ids_set(args.infile)
    access_token = get_access_token()
    posts = get_last_vk_posts_of_communities(access_token, page_ids)
    python_posts = get_good_posts(posts, is_python_post)
    python_stripped_posts = strip_vk_posts(python_posts)
    store_to_database(python_stripped_posts, args.outfile)
