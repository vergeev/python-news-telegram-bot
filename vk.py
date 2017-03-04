import os
import time
import requests


class VkRequestError(Exception): 
    def __init__(self, message, error_code):
        super(Exception, self).__init__('%d: %s' % (error_code, message))
        self.error_code = error_code


def get_access_token():
    return os.environ.get('VK_ACCESS_TOKEN')


def raise_if_vk_error(json_response):
    if 'error' in json_response:
        error_code = json_response['error']['error_code']
        error_msg = json_response['error']['error_msg']
        raise VkRequestError(error_msg, error_code)


def make_vk_api_request(method, **params):
    method_url = 'https://api.vk.com/method/%s' % method
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    json_response = response.json() 
    raise_if_vk_error(json_response)
    return json_response


def invoke_with_cooldown(function, **kwargs):
    too_many_requests_error_code = 6
    cooldown_seconds = 2
    try:
        return function(**kwargs)
    except VkRequestError as e:
        if e.error_code != too_many_requests_error_code:
            raise
        time.sleep(cooldown_seconds)
        return function(**kwargs)


def groups_search(access_token, *, query, type, count=20):
    response = make_vk_api_request('groups.search', access_token=access_token,
                                   q=query, type=type, count=count)
    group_list = response['response'][1:]  # the first element is the number of groups
    return group_list


def wall_get(access_token, *, owner_id, filter, fields=None, count=10):
    response = make_vk_api_request('wall.get', access_token=access_token, fields=fields,
                                   owner_id=owner_id, filter=filter, count=count)
    post_list = response['response'][1:]  # the first element is the number of posts
    return post_list


def group_get_by_id(access_token, *, group_id, fields):
    response = make_vk_api_request('groups.getById', access_token=access_token,
                                   group_id=group_id, fields=fields)
    group = response['response']
    return group
