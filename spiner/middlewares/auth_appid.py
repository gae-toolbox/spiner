from spiner import config
from webapp2 import abort

TRUSTED_APP_IDS = config.getenv('TRUSTED_APP_IDS')


def auth_appid(func):
    """Trusted apps authorization handler method decorator

    This wrapper will recect all request comming from not whitelisted apps
    """
    def func_wrapper(self, *args, **kwargs):
        app_id = self.request.headers.get('X-Appengine-Inbound-Appid', None)
        if not config.is_local_env():
            if app_id not in TRUSTED_APP_IDS:
                abort(403, "App '{}' is not allowed".format(app_id))
        return func(self, *args, **kwargs)
    return func_wrapper
