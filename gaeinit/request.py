# -*- coding: utf-8 -*-
import json
import webapp2
import config

_intent = None
_separators = None
if config.is_debug_mode():
    _intent = 4
    _separators = (',', ': ')


class JsonRequestHandler(webapp2.RequestHandler):
    def _send(self, data, code=200):
        self.response.content_type = 'application/json'
        self.response.status = code
        self.response.write(json.dumps(data, sort_keys=True, indent=_intent,
                                       separators=_separators))
