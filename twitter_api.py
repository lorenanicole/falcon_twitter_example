__author__ = 'lorenamesa'

import requests
from requests_oauthlib import OAuth1
import falcon
from collections import defaultdict
import json

# https://dev.twitter.com/overview/api/response-codes
TWITTER_CODE_TO_FALCON_STATUS = defaultdict(lambda: falcon.HTTP_500, [(200, falcon.HTTP_200),
                                                                      (400, falcon.HTTP_400),
                                                                      (404, falcon.HTTP_404),
                                                                      (401, falcon.HTTP_401),
                                                                      (500, falcon.HTTP_500)])

class TwitterApi(object):

    base_url = 'https://api.twitter.com/1.1/'

    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_secret):
        self.client = OAuth1(consumer_key, consumer_secret, oauth_token, oauth_secret)

    def get_home_timeline(self, count=20):
        response = requests.get(self.base_url + 'statuses/home_timeline.json?count='.format(count), auth=self.client)
        if response.ok:
            return response.status_code, json.loads(response.content)

        return response.status_code, {"error": response.content}

    def post_status(self, status):

        response = requests.post(self.base_url + 'statuses/update.json',
                                 data={"status": status},
                                 auth=self.client)
        if response.ok:
            return response.status_code, json.loads(response.content)

        return response.status_code, {"error": response.content}