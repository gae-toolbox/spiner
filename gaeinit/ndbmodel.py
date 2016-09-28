from google.appengine.ext import ndb


class Model(ndb.Model):
    """Generic ndb model"""

    updatetime = ndb.DateTimeProperty(auto_now=True)
    createtime = ndb.DateTimeProperty(auto_now_add=True)

    def get_id(self):
        """Returns key ID"""
        return self.key.id() if self.key else None

    def to_dict(self):
        """Returns ndb model as dictionary"""
        d = {}
        for k, v in super(Model, self).to_dict().iteritems():
            if isinstance(v, ndb.Key):
                v = v.get().to_dict()
            d[k] = v
        d['id'] = self.get_id()
        return d
