import re
import json
import requests
import requests_cache
from datetime import timedelta
from .api_data import API_ROOT, USER_ROOT, DOWNLOAD_ROOT


# Setup cache for requests
requests_cache.install_cache(expire_after=timedelta(hours=24))


class ReplIt():

    def __init__(self, username, number_to_retreive=9999):
        self.username = username  # Omit the @
        self.count = number_to_retreive  # Number of entries to get in GraphQL query
        self.data = self.setup()


    def setup(self) -> list:
        '''Get the initial repl data from the GraphQL API'''
        repls = requests.post(f'{API_ROOT}', 
                                    json=self.create_data(), headers=self.create_headers())
        this_data = json.loads(repls.text)
        return [item for item in this_data['data']['user']['repls']['items']]

    
    def get_urls(self) -> list:
        '''Returns only the urls in the JSON data we collect''' 
        return [item['url'] for item in self.data]


    def download_zip(self, url) -> bool:
        '''Receives a URL from the GraphQL JSON; downloads the file and returns True on success'''
        dl = requests.get(f'{DOWNLOAD_ROOT}/{url}.zip')
        if dl.status_code != requests.codes.ok:
            return False
        return True

    def create_headers(self) -> dict:
        '''Create headers for the request'''
        return {'referrer': f'{USER_ROOT}{self.username}'}


    def create_data(self) -> dict:
        return {
            "operationName": "userByUsername",
            "variables": {
                "username": self.username,
                "pinnedReplsFirst": 'true',
                "count": self.count
                # "after": "MjAxOS0wMS0zMFQyMjo1Mzo0NC4zMTha"
            },
            "query": '''query userByUsername($username: String!, $pinnedReplsFirst: Boolean, $count: Int, $after: String, $before: String, $direction: String, $order: String) {\n  user: userByUsername(username: $username) {\n    id\n    username\n    firstName\n    displayName\n    isLoggedIn\n    repls: publicRepls(pinnedReplsFirst: $pinnedReplsFirst, count: $count, after: $after, before: $before, direction: $direction, order: $order) {\n      items {\n        id\n        timeCreated\n        pinnedToProfile\n        ...ProfileReplItemRepl\n        __typename\n      }\n      pageInfo {\n        hasNextPage\n        nextCursor\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProfileReplItemRepl on Repl {\n  id\n  ...ReplItemBaseRepl\n  __typename\n}\n\nfragment ReplItemBaseRepl on Repl {\n  id\n  url\n  title\n  languageDisplayName\n  timeCreated\n  __typename\n}\n'''
        }
