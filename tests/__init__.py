# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from google.appengine.ext import testbed
import unittest
import webapp2
import webtest

webapp = webapp2.WSGIApplication()


class BaseTestCase(unittest.TestCase):
    """Abstract test case"""

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_files_stub()
        self.testbed.init_app_identity_stub()
        self.testbed.init_urlfetch_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_blobstore_stub()
        self.testapp = webtest.TestApp(webapp)
        self.testbed.init_mail_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()
