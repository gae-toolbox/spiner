# -*- coding: utf-8 -*-

"""Taken from: http://goo.gl/JmX4At"""
from google.appengine.ext import ndb
from time import mktime
import webapp2
import webapp2_extras


class User(webapp2_extras.appengine.auth.models.User):
    def set_password(self, raw_password):
        """Sets the password for the current user

        :param raw_password:
            The raw password which will be hashed and stored
        """
        self.password = webapp2_extras.security.generate_password_hash(
            raw_password, length=12)

    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        """Returns a user object based on a user ID and token.

        :param user_id:
            The user_id of the requesting user.
        :param token:
            The token string to be verified.
        :returns:
            A tuple ``(User, timestamp)``, with a user object and
            the token timestamp, or ``(None, None)`` if both were not found.
        """
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        # Use get_multi() to save a RPC call.
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None


class SessionRequestHandler(webapp2.RequestHandler):
    """Adds support for user session to default request handler"""
    @webapp2.cached_property
    def session(self):
        """Shortcut to access the current session."""
        return self.session_store.get_session(backend="datastore")

    @webapp2.cached_property
    def auth(self):
        """Shortcut to access the auth instance as a property."""
        return webapp2_extras.auth.get_auth()

    @webapp2.cached_property
    def user_model(self):
        """Shortcut to access the user model instance as a property."""
        return self.auth.store.user_model

    @webapp2.cached_property
    def current_user(self):
        """Shortcut to access the current logged in user.

        It fetches information from the persistence layer and
        returns an instance of the underlying model.

        :returns
            The instance of the user model associated to the logged in user.
        """
        u = self.auth.get_user_by_session()
        return self.user_model.get_by_id(
            u['user_id']) if u else None

    def dispatch(self):
        """Wrap request with session manager"""
        self.session_store = webapp2_extras.sessions.get_store(
                request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)


def user_required(handler):
    """Handler method decorator that checks if there's a user associated
    with the current session.  Will also fail if there's no session present.
    """
    def check_login(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            self.redirect(self.uri_for('signin'), abort=True)
        else:
            return handler(self, *args, **kwargs)

    return check_login
