"""Config helper

Allows to overwrite base config params from app.yaml with
dev.yaml and local.yaml file

To access those config values you can use

    config.getenv(key)

Module has few additional helper methods
"""
from google.appengine.api import app_identity
import os
import yaml


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

# memorize system env variables
_settings = {}
_prod_env = yaml.load(file('app.yaml', 'r'))['env_variables']

# Overwrite production settings for dev environments
if (is_cli_mode() or is_local_env()) and os.path.isfile('local.yaml'):
    env = yaml.load(file('local.yaml', 'r'))['env_variables']
    for (k, v) in dict(_prod_env, **env).items():
        _settings[k] = v
    _settings['ENVIRONMENT'] = 'development'
else:
    if is_dev_env() and os.path.isfile('dev.yaml'):
        env = yaml.load(file('dev.yaml', 'r'))['env_variables']
        for (k, v) in dict(_prod_env, **env).items():
            _settings[k] = v
        _settings['ENVIRONMENT'] = 'development'
    else:
        for (k, v) in _prod_env.items():
            _settings[k] = v
        _settings['ENVIRONMENT'] = 'production'
