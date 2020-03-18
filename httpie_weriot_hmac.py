"""
WeRiot HMAC Auth plugin for HTTPie.

Heavily based on https://github.com/jakubroztocil/httpie
"""
import datetime
import base64
import hashlib
import hmac

from httpie.plugins import AuthPlugin

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

__version__ = '0.1.0'
__author__ = 'David De Sousa'
__licence__ = 'MIT'


class HmacAuth:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key.encode('ascii')

    def __call__(self, r):
        method = r.method

        content_type = r.headers.get('content-type')
        if not content_type:
            content_type = ''
        else:
            content_type = content_type.decode('utf-8')

        content_hash = r.headers.get('content-hash')
        if not content_hash:
            if isinstance(r.body, bytes):
                content = r.body
            elif r.body:
                content = r.body.encode('utf-8')
            else:
                content = b''
            content_hash = hashlib.sha256(content).hexdigest()

        httpdate = r.headers.get('date')
        if not httpdate:
            httpdate = datetime.datetime.utcnow().isoformat()
            r.headers['Date'] = httpdate
        else:
            httpdate = httpdate.decode('utf-8')

        url = urlparse(r.url)
        path = url.path

        string_to_sign = '\n'.join([
            method,
            content_hash,
            content_type,
            httpdate,
            path,
        ]).encode('utf-8')
        digest = hmac.new(self.secret_key, string_to_sign,
                          hashlib.sha256).digest()
        signature = base64.encodestring(digest).rstrip().decode('utf-8')

        if self.access_key == '':
            r.headers['X-Signature'] = 'HMAC %s' % signature
        elif self.secret_key == '':
            raise ValueError('HMAC secret key cannot be empty.')
        else:
            r.headers['X-Signature'] = 'HMAC %s:%s' % (self.access_key,
                                                       signature)

        return r


class WeriotHmacPlugin(AuthPlugin):

    name = 'WeRiot HMAC signature auth'
    auth_type = 'weriot-signature'
    description = 'Sign requests using a HMAC authentication method like AWS'

    def get_auth(self, username=None, password=None):
        return HmacAuth(username, password)
