__author__ = 'lorenamesa'

from talons.auth import basicauth, htpasswd
from falcon import HTTPUnauthorized

class Auth(object):
    '''
    Talons Middleware reworking of old Falcon (<= 0.4) hook to support Falcon 1.0.0 middleware syntax

    :param: **kwargs requires a htpasswd_path pathway for a local Apache htpasswd file.
    '''

    def __init__(self, **config):
        self.identifier = basicauth.Identifier()
        self.authenticator = htpasswd.Authenticator(**config)

    def process_request(self, req, res):
        parsed_identity = self.identifier.identify(req)
        if not parsed_identity:
            raise HTTPUnauthorized(title="Unauthorized",
                                   description="Cannot locate credentials in HTTP Authorization header.",
                                   challenges=["No credentials provided."])

        if not self.authenticator.authenticate(req.env['wsgi.identity']):
            raise HTTPUnauthorized(title="Unauthorized",
                                   description="Credentials provided incorrect.",
                                   challenges=["Incorrect credentials provided."])