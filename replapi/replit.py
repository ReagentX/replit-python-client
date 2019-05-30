import json
import os
import re
import shutil
import sys
import zipfile
from datetime import timedelta
from multiprocessing.dummy import Pool as ThreadPool

import requests
import requests_cache

from .api_data import API_ROOT, DOWNLOAD_ROOT, USER_ROOT

# Setup cache for requests
requests_cache.install_cache(expire_after=timedelta(hours=2))


class ReplIt():

    def __init__(self, username, number_to_retreive=999):
        self.username = username  # Omit the @
        self.create_folder(self.username)
        self.count = number_to_retreive  # Number of entries to get in GraphQL query
        self.data = self.setup()


    def create_folder(self, name) -> None:
        '''Create user folder to download files into'''
        if not os.path.exists(name):
            os.makedirs(name)


    def setup(self) -> list:
        '''Get the initial repl data from the GraphQL API'''
        repls = requests.post(f'{API_ROOT}', 
                              json=self.create_data(), headers=self.create_headers())
        this_data = json.loads(repls.text)
        return [item for item in this_data['data']['user']['repls']['items']]


    def get_urls(self) -> list:
        '''Returns only the urls in the JSON data we collect''' 
        return [item['url'] for item in self.data]


    def download_all(self, threads=32) -> None:
        '''Handles multiprocessing using ThreadPool; sends items from a list to a function and gets the results as a list'''
        pool = ThreadPool(threads)
        lst = self.get_urls()
        print(f"Downloading {len(lst)} items using {self.download_zip} in {threads} processes.")
        result = (pool.imap_unordered(self.download_zip, lst))
        pool.close()

        # Display progress as the scraper runs its processes
        while (len(lst) > 1):
            completed = result._index
            # Break out of the loop if all tasks are done or if there is only one task
            if (completed == len(lst)):
                sys.stdout.flush()
                sys.stdout.write('\r' + "")
                sys.stdout.flush()
                break
            # Avoid a ZeroDivisionError
            if completed > 0:
                sys.stdout.flush()
                sys.stdout.write('\r' + f"{completed/len(lst)*100:.0f}% done. {len(lst)-completed} left. ")
                sys.stdout.flush()
            sys.stdout.flush()
        pool.join()
        return list(result)


    def download_zip(self, slug) -> bool:
        '''Receives a slug from the GraphQL JSON; downloads the file and returns the slug if the download fails'''
        dl = requests.get(f'{DOWNLOAD_ROOT}{slug}.zip', stream=True)
        if dl.status_code == requests.codes.ok:
            filepath = f'{self.username}/{slug.split("/")[-1]}'
            self.create_folder(filepath)
            with open(filepath + '/z.zip', 'wb') as f:
                shutil.copyfileobj(dl.raw, f)
            # Unzip and remove
            self.unzip(filepath)
            os.remove(filepath + '/z.zip')
            return None
        return slug


    def unzip(self, path: str) -> None:
        '''Unzip file passed as the `path` string'''
        z = zipfile.ZipFile(path + '/z.zip', 'r')
        z.extractall(path)
        z.close()


    def create_headers(self) -> dict:
        '''Create headers for the request'''
        return {'referrer': f'{USER_ROOT}{self.username}'}


    def create_data(self) -> dict:
        '''Creates the GraphQL query for a request object'''
        return {
            "operationName": "userByUsername",
            "variables": {
                "username": self.username,
                "pinnedReplsFirst": 'true',
                "count": self.count
            },
            "query": '''query userByUsername($username: String!, $pinnedReplsFirst: Boolean, $count: Int, $after: String, $before: String, $direction: String, $order: String) {\n  user: userByUsername(username: $username) {\n    id\n    username\n    firstName\n    displayName\n    isLoggedIn\n    repls: publicRepls(pinnedReplsFirst: $pinnedReplsFirst, count: $count, after: $after, before: $before, direction: $direction, order: $order) {\n      items {\n        id\n        timeCreated\n        pinnedToProfile\n        ...ProfileReplItemRepl\n        __typename\n      }\n      pageInfo {\n        hasNextPage\n        nextCursor\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProfileReplItemRepl on Repl {\n  id\n  ...ReplItemBaseRepl\n  __typename\n}\n\nfragment ReplItemBaseRepl on Repl {\n  id\n  url\n  title\n  languageDisplayName\n  timeCreated\n  __typename\n}\n'''
        }
