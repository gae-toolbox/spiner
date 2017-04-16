# -*- coding: utf-8 -*-

from webapp2 import uri_for
from webapp2_extras import sessions


def auth_session(func):
    """Auth request only when session is open and not expired"""
    def func_wrapper(self, *args, **kwargs):
        store = sessions.get_store(request=self.request)

        session = store.get_session()

        if not session:
            self.redirect(uri_for('signin', **kwargs))
            return
        return func(self, session=session, *args, **kwargs)
    return func_wrapper
