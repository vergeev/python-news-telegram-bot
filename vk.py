import os
import json
import requests

def make_vk_api_request(method, **params):
    method_url = 'https://api.vk.com/method/%s' % method
    response = requests.get(method_url, params=params)
    return response.json()

#def groups_search(access_token, *, query, type, count=20):
