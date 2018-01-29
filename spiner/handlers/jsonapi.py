# -*- coding: utf-8 -*-
from jsonschema import ValidationError
import json
import logging
import spiner.config
import webapp2


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

def client_error(request, response, exception):
    response.headers.add_header('Content-Type', 'application/json')
    code = exception.code if hasattr(exception, 'code') else 400

    if spiner.config.is_debug_mode():
        logging.exception(exception)

    try:
        error_desc = getattr(errorcodes, str(exception.message))
        error_code = exception.message
    except (AttributeError, NameError):
        error_desc = exception.message
        error_code = None

    msg = {
        'status': 'ERROR',
        'status_code': code,
        'status_message': response.http_status_message(code),
        'body': error_desc,
        'error_code': error_code,
    }

    response.write(json.dumps(msg, sort_keys=True))
    response.set_status(code)


def internal_server_error(request, response, exception):
    if isinstance(exception, ValidationError):
        return client_error(response, response, exception)

    logging.exception(exception)

    response.headers.add_header('Content-Type', 'application/json')

    response.set_status(500)
    msg = {
        'status': 'ERROR',
        'status_code': 500,
        'status_message': response.http_status_message(500),
        'body': exception.message
    }

    if spiner.config.is_debug_mode():
        msg['debug_info'] = str(exception)

    response.write(json.dumps(msg, sort_keys=True))
