import bcrypt
from spiner.config import getenv

BCRYPT_ROUNDS = int(getenv('BCRYPT_ROUNDS'))


def hash(pwd, salt=None):
    """Returns encrypted password"""
    if not salt:
        salt = bcrypt.gensalt(BCRYPT_ROUNDS)
    return bcrypt.hashpw(pwd, salt)
