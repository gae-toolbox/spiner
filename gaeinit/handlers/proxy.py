from gaeinit.config import getenv
from google.appengine.api import urlfetch
from webapp2 import RequestHandler

TIMEOUT = getenv('GAEINIT_HTTPPROXY_TIMEOUT')


class Handler(RequestHandler):
    """HTTP proxy handler

    Usage example for example route:

        Route('/proxy', handler=Handler, name='proxy')

    example request:

        /proxy?url=http://example.com
    """
    def get(self):
        url = self.request.get('url')
        if not url:
            self.abort(
                400,
                "'url' parameter is mandatory, ...?url=http://example.com")
        self._build_response(urlfetch.fetch(
            deadline=TIMEOUT,
            follow_redirects=False,
            url=url))

    def put(self):
        url = self.request.get('url')
        self._build_response(urlfetch.fetch(
            method=urlfetch.PUT,
            deadline=TIMEOUT,
            follow_redirects=False,
            payload=self.request.body,
            url=url))

    def post(self):
        url = self.request.get('url')
        self._build_response(urlfetch.fetch(
            method=urlfetch.POST,
            deadline=TIMEOUT,
            follow_redirects=False,
            payload=self.request.body,
            url=url))

    def _build_response(self, response):
        self.response.body = response.content
        self.response.status = response.status_code
        self.response.headers = response.headers
        self.response.headers['X-Proxy'] = 'YES'
