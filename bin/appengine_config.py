"""
`appengine_config.py` is automatically loaded when Google App Engine
starts a new instance of your application. This runs before any
WSGI applications specified in app.yaml are loaded.
"""

from google.appengine.ext import vendor
import os

# Third-party libraries are stored in "lib", vendoring will make
# sure that they are importable by the application.
if os.path.isdir(os.path.join(os.getcwd(), 'lib')):
    vendor.add('lib')

# Fix for https://code.google.com/p/googleappengine/issues/detail?id=2440#c20
# remote_api authentication should be "bypassable" on local dev server
# http://127.0.0.1:8080/_ah/remote_api
if os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
    remoteapi_CUSTOM_ENVIRONMENT_AUTHENTICATION = (
        'REMOTE_ADDR', ['127.0.0.1'])
