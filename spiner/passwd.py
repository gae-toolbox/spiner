import bcrypt
from spiner.config import getenv


def hash(pwd, salt=None):
    """Returns encrypted password"""
    if not salt:
        salt = bcrypt.gensalt(int(getenv('BCRYPT_ROUNDS')))
    return bcrypt.hashpw(pwd, salt)
