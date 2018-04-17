import ast
import json

__author__ = 'lorenamesa'

import requests
from requests_oauthlib import OAuth1
import falcon


# https://dev.twitter.com/overview/api/response-codes
TWITTER_CODE_TO_FALCON_STATUS = {
                                    200: falcon.HTTP_200,
                                    400: falcon.HTTP_400,
                                    404: falcon.HTTP_404,
                                    401: falcon.HTTP_401,
                                    429: falcon.HTTP_429,
                                    500: falcon.HTTP_500
}


class TwitterApi(object):

    base_url = 'https://api.twitter.com/1.1/{}'

    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_secret):
        self.client = OAuth1(consumer_key, consumer_secret, oauth_token, oauth_secret)

    def get_home_timeline(self, count=20):
        url_suffix = 'statuses/home_timeline.json?count={}'.format(count)
        response = requests.get(self.base_url.format(url_suffix), auth=self.client)
        content = json.loads(ast.literal_eval(json.dumps(response.content.decode('utf8'))))

        if response.ok:
            if isinstance(content, dict) and content.get('errors'):
                return response.status_code, content

            return response.status_code, content

        return response.status_code, content

    def post_status(self, status):

        response = requests.post(self.base_url.format('statuses/update.json'),
                                 data={'status': status},
                                 auth=self.client)
        content = response.json()
        if response.ok:
            return response.status_code, content

        return response.status_code, content