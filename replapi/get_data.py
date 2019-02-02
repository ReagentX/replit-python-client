import re
import requests
import requests_cache
from datetime import timedelta
from api_data import API_ROOT, USER_ROOT


# Setup cache for requests
requests_cache.install_cache(expire_after=timedelta(hours=24))


class ReplIt():

    def __init__(self, username):
        self.username = username  # Omit the @
        self.data = self.setup()


    def setup(self):
        homepage_user_data = requests.get(f'{USER_ROOT}{self.username}')
        repls = re.findall(f'/@{self.username}/.*?\"', homepage_user_data.text)
        print(repls, len(repls))
        if len(repls) > 20:
            raise ValueError(f'Too many regex matches, got {len(repls)}, expected 20.')
        if len(repls) < 20:
            return repls
        else:
            next_repls = 


    def create_headers(self):
        {
            "operationName": "userByUsername",
            "variables": {
                "username": f"{self.username}",
                "pinnedReplsFirst": true
                # "after": "MjAxOS0wMS0zMFQyMjo1Mzo0NC4zMTha"
            },
            "query": "query userByUsername($username: String!, $pinnedReplsFirst: Boolean, $count: Int, $after: String, $before: String, $direction: String, $order: String) {\n  user: userByUsername(username: $username) {\n    id\n    username\n    firstName\n    displayName\n    isLoggedIn\n    repls: publicRepls(pinnedReplsFirst: $pinnedReplsFirst, count: $count, after: $after, before: $before, direction: $direction, order: $order) {\n      items {\n        id\n        timeCreated\n        pinnedToProfile\n        ...ProfileReplItemRepl\n        __typename\n      }\n      pageInfo {\n        hasNextPage\n        nextCursor\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProfileReplItemRepl on Repl {\n  id\n  ...ReplItemBaseRepl\n  __typename\n}\n\nfragment ReplItemBaseRepl on Repl {\n  id\n  url\n  title\n  languageDisplayName\n  timeCreated\n  __typename\n}\n"
        }



r = ReplIt('reagentx')
