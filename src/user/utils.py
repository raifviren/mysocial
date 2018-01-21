import base64
import binascii
import collections
import hashlib
import hmac
import os
import random
import time
import urllib
import urllib.parse

import oauth2

from .constants import TWITTER_REQUEST_TOKEN_URL


def get_consumer_twitter():
    # Set the consumer key and secret
    CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']

    # Create a oauth2.Consumer object that wraps the parameters for the calls to the HTTP endpoints
    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    return consumer


def get_request_token():
    consumer = get_consumer_twitter()
    # Use the oauth2.Client class to call the Twitter OAuth endpoint
    resp, content = oauth2.Client(consumer).request(TWITTER_REQUEST_TOKEN_URL, "GET")

    # Create a standard dictionary from the response body, using parse_qsl as a convenience to parse the query string in the response
    request_token = dict(urllib.parse.parse_qsl(content))
    print(request_token)
    # print(request_token.get(b'oauth_token'))
    oauth_token = request_token.get(b'oauth_token').decode("utf-8")
    oauth_token_secret = request_token.get(b'oauth_token_secret').decode("utf-8")
    return oauth_token, oauth_token_secret


def escape(s):
    """Percent Encode the passed in string"""
    return urllib.parse.quote(s, safe='~')


def get_nonce():
    """Unique token generated for each request"""
    n = base64.b64encode(
        ''.join([str(random.randint(0, 9)) for i in range(24)]).encode())
    return n


def generate_signature(method, url, url_parameters, oauth_parameters,
                       oauth_consumer_key, oauth_consumer_secret,
                       oauth_token_secret=None, status=None):
    """Create the signature base string"""

    # Combine parameters into one hash
    temp = collect_parameters(oauth_parameters, status, url_parameters)

    # Create string of combined url and oauth parameters
    parameter_string = stringify_parameters(temp)

    # Create your Signature Base String
    signature_base_string = (
            method.upper() + '&' +
            escape(str(url)) + '&' +
            escape(parameter_string)
    ).encode('utf-8')

    # Get the signing key
    signing_key = create_signing_key(oauth_consumer_secret, oauth_token_secret)

    return calculate_signature(signing_key, signature_base_string)


def collect_parameters(oauth_parameters, status, url_parameters):
    """Combines oauth, url and status parameters"""
    # Add the oauth_parameters to temp hash
    temp = oauth_parameters.copy()

    # Add the status, if passed in.  Used for posting a new tweet
    if status is not None:
        temp['status'] = status
    print(url_parameters)
    # Add the url_parameters to the temp hash
    for k, v in url_parameters.items():
        print(k, v)
        temp[k] = v

    return temp


def calculate_signature(signing_key, signature_base_string):
    """Calculate the signature using SHA1"""
    # signing_key = signing_key.encode('utf-8')
    hashed = hmac.new(
        signing_key, signature_base_string, hashlib.sha1)

    sig = binascii.b2a_base64(hashed.digest())[:-1]

    return escape(sig)


def create_signing_key(oauth_consumer_secret, oauth_token_secret=None):
    """Create key to sign request with"""
    signing_key = escape(oauth_consumer_secret) + '&'

    if oauth_token_secret is not None:
        signing_key += escape(oauth_token_secret)

    return signing_key.encode('utf-8')


def create_auth_header(parameters):
    """For all collected parameters, order them and create auth header"""
    ordered_parameters = {}
    ordered_parameters = collections.OrderedDict(sorted(parameters.items()))
    auth_header = (
        '%s="%s"' % (k, v) for k, v in ordered_parameters.items())
    val = "OAuth " + ', '.join(auth_header)
    return val


def stringify_parameters(parameters):
    """Orders parameters, and generates string representation of parameters"""
    output = ''
    ordered_parameters = {}
    ordered_parameters = collections.OrderedDict(sorted(parameters.items()))
    print(ordered_parameters)
    counter = 1
    for k, v in ordered_parameters.items():
        print(k, v)
        output += escape(str(k)) + '=' + escape(str(v))
        if counter < len(ordered_parameters):
            output += '&'
            counter += 1

    return output


def get_oauth_parameters(consumer_key, access_token):
    """Returns OAuth parameters needed for making request"""
    oauth_parameters = {
        'oauth_timestamp': str(int(time.time())),
        'oauth_signature_method': "HMAC-SHA1",
        'oauth_version': "1.0",
        # 'oauth_token': access_token,
        'oauth_callback': "http%3A%2F%2Flocalhost%2Fsign-in-with-twitter%2F",
        'oauth_nonce': get_nonce(),
        'oauth_consumer_key': consumer_key
    }

    return oauth_parameters
