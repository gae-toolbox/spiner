# -*- coding: utf-8 -*-
"""Abstract handler for all handlers with session support"""

from webapp2_extras import sessions
import re
import webapp2


class Handler(webapp2.RequestHandler):
    def initialize(self, request, response):
        super(Handler, self).initialize(request, response)
        match = re.match('^(http[s]?://)www\.(.*)', request.url)
        if match:
            self.redirect(match.group(1) + match.group(2), permanent=True)

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()
