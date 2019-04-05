# -*- coding: utf-8 -*-
from google.appengine.ext.webapp import blobstore_handlers
import spiner
import spiner.env


class Handler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        """Copy uploaded files to provided destination

        Returns:
            string: path to uploaded path
        """
        if not self.get_file_infos():
            self.abort(400, "No file has been uploaded")

        fileinfo = self.get_file_infos()[0]

        try:
            import cloudstorage as gcs
        except ImportError:
            self.abort(
                    500,
                    'GoogleAppEngineCloudStorageClient module is required')

        stat = gcs.stat(fileinfo.gs_object_name[3:])
        destpath = "/".join(stat.filename.split("/")[:-1])

        gcs.copy2(fileinfo.gs_object_name[3:], destpath)
        gcs.delete(fileinfo.gs_object_name[3:])

        if spiner.env.is_local_env():
            url = '/_ah/gcs{}'.format(destpath)
        else:
            url = 'https://storage.googleapis.com{}'.format(destpath)

        self.response.write(url)
