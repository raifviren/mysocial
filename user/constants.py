import os
from decouple import config

TWITTER_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
TWITTER_AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'
TWITTER_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
INSTA_AUTHORIZE_URL = 'https://api.instagram.com/oauth/authorize/'
INSTA_ACCESS_TOKEN_URL = 'https://api.instagram.com/oauth/access_token'
INSTA_COMMENTS_URL = 'https://api.instagram.com/v1/media/{0}/comments?access_token={1}'
INSTA_MEDIA_URL = 'https://api.instagram.com/v1/media/{0}?access_token={1}'
INSTA_TIMELINE_URL = 'https://api.instagram.com/v1/users/self/media/recent/?access_token={0}&count={1}'
INSTA_LIKED_URL = 'https://api.instagram.com/v1/users/self/media/liked?access_token={0}'
INSTA_CALLBACK_URL = config('INSTA_CALLBACK_URL')
