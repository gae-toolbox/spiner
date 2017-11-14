# -*- coding: utf-8 -*-

import webapp2
import json
import spiner.config


class Error(Exception):
    pass


class InvalidJsonInRequestBody(Error):
    pass


class Handler(webapp2.RequestHandler):
    """Base Json handler
    """
    def _decode_req_payload(self):
        """Returns encoded json from request body"""
        try:
            return json.loads(self.request.body)
        except ValueError:
            raise InvalidJsonInRequestBody('Malformed JSON in request body')

    def _send(self, data, code=200, doc=None):
        intent = None
        separators = None
        if spiner.config.is_debug_mode():
            intent = 4
            separators = (',', ': ')
        self.response.content_type = 'application/json'
        self.response.status = code
        res = {
            'status': 'SUCCESS',
            'status_code': code,
            'data': data
            }

        if doc:
            res['doc'] = doc

        self.response.write(json.dumps(
            res, sort_keys=True, indent=intent, separators=separators))


def response_schema(data_schema={}):
    return {
        "name": "json response",
        "type": "object",
        "properties": {
            "code": {"type": "string"},
            "data": data_schema,
        },
        "required": [
            "code",
            "data",
            "message",
            "description",
        ]
    }
