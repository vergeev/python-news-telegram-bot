import os
import requests


class VkRequestError(Exception): pass


def make_vk_api_request(method, **params):
    method_url = 'https://api.vk.com/method/%s' % method
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    return response.json()


def raise_if_vk_error(json_response):
    if 'error' in json_response:
        error_code = json_response['error']['error_code']
        error_msg = json_response['error']['error_msg']
        raise VkRequestError("%d: %s" % (error_code, error_msg))


def groups_search(access_token, *, query, type, count=20):
    response = make_vk_api_request('groups.search', access_token=access_token,
                                   q=query, type=type, count=count)
    raise_if_vk_error(response)
    return response['response'][1:]
