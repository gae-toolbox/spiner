# -*- coding: utf-8 -*-

import webapp2
import json


class Error(Exception):
    pass


class InvalidJsonInRequestBody(Error):
    pass


class Handler(webapp2.RequestHandler):
    """Base Json handler
    """
    def _get_req_json_body(self):
        """Returns encoded json from request body"""
        try:
            return json.loads(self.request.body)
        except ValueError:
            raise InvalidJsonInRequestBody('Malformed JSON in request body')


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
