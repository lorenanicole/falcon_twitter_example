import json
import falcon
import yaml
from middleware.auth import Auth
import os
from twitter_api import TwitterApi, TWITTER_CODE_TO_FALCON_STATUS
import falcon_jsonify

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG = yaml.load(open('{}/{}'.format(BASE_DIR, '/config.yml'), 'r'))


app = falcon.API(middleware=[Auth(**CONFIG), falcon_jsonify.Middleware(help_messages=True)])


def validate_query_params(req, resp, resource, params):
    count = int(req.get_param('count'))

    if not 1 <= count <= 200:
        msg = 'Please request between 1 to 200 tweets.'
        raise falcon.HTTPBadRequest('Bad request', msg)

class Resource(object):

    def on_get(self, req, resp):

        if req._params.get('name'):
            resp_msg = "Hello {0}!".format(req._params.get('name'))
        else:
            resp_msg = "Hello world!"
        resp.body = '{"message": "' + resp_msg + '"}'
        resp.status = falcon.HTTP_200


class TwitterResource(object):

    def __init__(self):
        self.twitter_api = TwitterApi(consumer_key=CONFIG.get('consumer_key'),
                                      consumer_secret=CONFIG.get('consumer_secret'),
                                      oauth_token=CONFIG.get('oauth_token'),
                                      oauth_secret=CONFIG.get('oauth_secret'))

class TwitterTimelineResource(TwitterResource):

    @falcon.before(validate_query_params)  # Decorator to validate params before processing request
    def on_get(self, req, resp):

        count = int(req.get_param('count'))

        if count:
            status_code, response = self.twitter_api.get_home_timeline(count)
        else:
            status_code, response = self.twitter_api.get_home_timeline()

        if isinstance(response, dict) and response.get('errors'):
            resp.status = TWITTER_CODE_TO_FALCON_STATUS[status_code]
            resp.json = response

        if status_code is 200:
            resp.status = TWITTER_CODE_TO_FALCON_STATUS[status_code]
            resp.json = {'statuses': response}

        resp.content_type = 'application/json; charset=utf-8'


class TwitterStatusResource(TwitterResource):

    def on_post(self, req, resp):

        status = json.loads(req.stream.read()).get('status')
        if not status or len(status) > 140 :
            msg = 'Status must be between 1 to 140 characters in length.'
            raise falcon.HTTPBadRequest('Bad request', msg)

        status_code, status = self.twitter_api.post_status(status)

        resp.status = TWITTER_CODE_TO_FALCON_STATUS[status_code]
        resp.json = status
        resp.content_type = 'application/json; charset=utf-8'

# Registering Routes

app.add_route('/example', Resource())  # Test Endpoint
app.add_route('/timeline', TwitterTimelineResource())
app.add_route('/status', TwitterStatusResource())

