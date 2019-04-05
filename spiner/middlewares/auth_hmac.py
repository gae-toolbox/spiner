# -*- coding: utf-8 -*-

from hashlib import md5
from webapp2 import abort
import spiner.env
import hmac
import re
import time


def auth_hmac(func):
    """HMAC authorization handler method decorator

    To sign requst you need to generate hmac-md5 with

    msg = relative url (path + query_string)
    key = spiner.env.getenv('HMAC_SECRET_KEY') +
            (current_timestamp - current_timestamp % 1000)

    Example of signed url:

    /uri/path?param1=1&param2=2&hmac=fa0ed6c31a72d71413bba43ef93582ca
    """
    def func_wrapper(self, *args, **kwargs):
        SECRET_KEY = spiner.env.getenv('HMAC_SECRET_KEY')
        EXPIRE = int(spiner.env.getenv('HMAC_EXPIRE'))
        auth = self.request.get('hmac', '')
        current_timestamp = int(time.time())
        expire = current_timestamp - current_timestamp % EXPIRE
        query_string = re.sub(
            r"[&?]?hmac=[0-9a-z]*",
            "",
            self.request.query_string
        )
        msg = (self.request.path + '?' + query_string).rstrip('?')

        code = hmac.new(
            SECRET_KEY + str(expire), msg, md5
        ).hexdigest()

        if spiner.env.is_debug_mode() and auth == 'bypass':
            auth = code

        if not auth:
            abort(403, 'Missing hmac parameter')

        if code != auth:
            if spiner.env.is_debug_mode():
                abort(403, 'Invalid hmac code. Should be: %s' % code)
            else:
                abort(403, 'Invalid hmac authorization code')

        return func(self, *args, **kwargs)

    return func_wrapper
