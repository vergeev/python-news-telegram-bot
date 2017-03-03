import os
import requests


class VkRequestError(Exception): pass


def raise_if_vk_error(json_response):
    if 'error' in json_response:
        error_code = json_response['error']['error_code']
        error_msg = json_response['error']['error_msg']
        raise VkRequestError("%d: %s" % (error_code, error_msg))


def make_vk_api_request(method, **params):
    method_url = 'https://api.vk.com/method/%s' % method
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    json_response = response.json() 
    raise_if_vk_error(json_response)
    return json_response


def groups_search(access_token, *, query, type, count=20):
    response = make_vk_api_request('groups.search', access_token=access_token,
                                   q=query, type=type, count=count)
    group_list = response['response'][1:]  # the first element is the number of groups
    return group_list
