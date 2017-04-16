# -*- coding: utf-8 -*-

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore


class Handler(blobstore_handlers.BlobstoreDownloadHandler):

    def get(self):
        """Serve blob

        URL params:
            path: path to file starting with bucket name /<bucket>/file...


        Example:

            webapp2.Route(
                '/_blob',
                handler=spiner.handlers.blob.Handler,
                name='blob'),

            uri_for('blob', path='/mybucket/path/to/file')
        """
        path = self.request.get('path')
        blobkey = blobstore.create_gs_key('/gs' + path)
        self.send_blob(blobkey)
