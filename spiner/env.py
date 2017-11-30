"""
"""
from google.appengine.api import app_identity
import os

def is_test_mode():
    """Returns True when application is running in unittest environment"""
    return os.environ['APPLICATION_ID'] == 'testbed-test'


def is_cli_mode():
    """Returns True when application is running in cli environment"""
    return 'SERVER_SOFTWARE' not in os.environ


def is_debug_mode():
    """Returns True when application is running in debug mode"""
    return bool(int(_settings['DEBUG']))


def is_prod_env():
    """Returns True when application is running in production mode"""
    return _settings['ENVIRONMENT'] == 'production'


def is_dev_env():
    """Returns True when application is running in production mode"""
    return app_identity.get_application_id().endswith('-dev')


def is_local_env():
    """Returns True when application is running on dev server"""
    if 'SERVER_SOFTWARE' in os.environ:
        return os.environ['SERVER_SOFTWARE'].startswith('Dev')
    return False


def getenv(key):
    """Returns value of config key if exists or None othewise.
    Note: In debug mode getting non existing key will raise an UserWarning
    exception
    """
    try:
        return _settings[key]
    except KeyError:
        raise UserWarning(
            "'{}' key doesn't exist in 'system environment variable".format(
                key,
            )
        )


def _get_env_settings():
    try:
        import env_variables
        key = app_identity.get_application_id().upper().replace('-', '_')
        return getattr(env_variables, key)
    except ImportError:
        raise ImportError(
                "Missing app_variable module with app specific config params")
    except AttributeError:
        raise AttributeError(
                "Missing config for {}".format(key))

# memorize system env variables
_settings = _get_env_settings()
