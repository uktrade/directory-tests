from hashlib import sha256
import urlparse

from locust.clients import HttpSession

import requests
from requests import Response, Request
from requests.exceptions import (
    RequestException,
    MissingSchema,
    InvalidSchema,
    InvalidURL
)

from tests import settings


class AuthenticatedClient(HttpSession):
    def _send_request_safe_mode(self, method, url, **kwargs):
        kwargs.pop('allow_redirects', None)
        try:
            request = requests.Request(method=method, url=url, **kwargs)
            signed_request = self.sign_request(
                api_key=settings.API_CLIENT_KEY,
                prepared_request=request.prepare(),
            )
            return requests.Session().send(signed_request)
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except RequestException as e:
            r = LocustResponse()
            r.error = e
            r.status_code = 0  # with this status_code, content returns None
            r.request = Request(method, url).prepare() 
            return r

    def sign_request(self, api_key, prepared_request):
        url = urlparse.urlsplit(prepared_request.path_url)

        path = bytes(url.path)
        if url.query:
            path += bytes("?{}".format(url.query))

        salt = bytes(api_key)
        body = prepared_request.body or b""

        if isinstance(body, str):
            body = bytes(body)

        signature = sha256(path + body + salt).hexdigest()
        prepared_request.headers["X-Signature"] = signature

        return prepared_request


class AuthedClientMixin(object):
    def __init__(self):
        super(AuthedClientMixin, self).__init__()
        self.client = AuthenticatedClient(base_url=self.host)
