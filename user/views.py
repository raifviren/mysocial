import base64
import json
import os

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
# Create your views here.
from django.views.generic.base import View
import oauth2
from twython import Twython
import urllib
import urllib.parse

from .constants import TWITTER_AUTHORIZE_URL, TWITTER_ACCESS_TOKEN_URL, INSTA_AUTHORIZE_URL, INSTA_CALLBACK_URL, \
    INSTA_ACCESS_TOKEN_URL, INSTA_COMMENTS_URL, INSTA_MEDIA_URL, INSTA_TIMELINE_URL, INSTA_LIKED_URL
from .forms import LoginForm
from .models import User
from .utils import get_consumer_twitter, get_request_token
from decouple import config
from django.db import IntegrityError
request_token = {}
access_token = {}
oauth_token = ''
oauth_token_secret = ''


class HomeView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user is not None:
            return render(request, self.template_name, {'user': request.user})
        else:
            form = LoginForm()
            return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        print(request)
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                User.objects.get(username=username)
                user = authenticate(
                    username=username,
                    password=password
                )
                print(user)
                if user is None:
                    return render(request, self.template_name, {'form.password.errors': "Incorrect Password"})
                else:
                    return render(request, 'index.html', {'user': user})
            except User.DoesNotExist:
                try:
                    user = User.objects.create(username=username, password=password)
                    if user is not None:
                        return render(request, 'index.html', {'user': user})
                except IntegrityError:
                    return render(request, self.template_name, {'form.username.errors': "Username Already Taken"})


        else:
            return render(request, self.template_name, {'form.non_field_errors': "Invalid Request"})


class TwitterView(View):
    template_name = 'twitter_index.html'

    def get(self, request, *args, **kwargs):
        global oauth_token
        global oauth_token_secret
        oauth_token, oauth_token_secret = get_request_token()
        request.session['oauth_token'] = oauth_token
        request.session['oauth_token_secret'] = oauth_token_secret
        request.session.modified = True
        print(request.session['oauth_token'])
        print(request.session['oauth_token_secret'])
        return redirect(
            "%s?oauth_token=%s" % (TWITTER_AUTHORIZE_URL, oauth_token))


def post_a_tweet():
    client_key = 'V5mR4ZNsHR5zwkO1gOfBBW8hs'
    client_secret = 'CEH86eb7FwaDX1Se4QKxFOOct6Qrmt7C9rCfSAglJj5Ui2RiLk'
    key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    res = requests.post(auth_url, headers=auth_headers, data=auth_data)
    json_response = json.loads(res.content.decode('utf-8'))
    access_token = json_response['access_token']
    print(access_token)
    auth_url = '{}/1.1/statuses/user_timeline.json?count=100&screen_name=twitterapi'.format(base_url)

    auth_headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        # 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }
    res = requests.get(auth_url, auth_headers)
    res = requests.post(auth_url, headers=auth_headers, data=auth_data)
    print(res)
    print(res.content)


class TwitterCallbackView(View):
    template_name = 'twitter_index.html'

    def get(self, request, *args, **kwargs):
        if 'oauth_verifier' not in request.GET:
            return HttpResponseRedirect(reverse('mysocial-index'))
        print(request)
        consumer = get_consumer_twitter()
        global oauth_token
        global oauth_token_secret
        token = oauth2.Token(oauth_token, oauth_token_secret)
        print(request.GET.get('oauth_verifier'))
        token.set_verifier(request.GET.get('oauth_verifier'))
        client = oauth2.Client(consumer, token)

        # Call the Twitter access token endpoint
        resp, content = client.request(TWITTER_ACCESS_TOKEN_URL, "POST")

        # Create a standard dictionary from the response body, using parse_qsl as a convenience to parse the query string in the response
        access_token = dict(urllib.parse.parse_qsl(content))
        print(access_token)
        if b'user_id' in access_token:
            user_id = access_token[b'user_id'].decode("utf-8")
            screen_name = access_token[b'screen_name'].decode("utf-8")
            oauth_token = access_token[b'oauth_token'].decode("utf-8")
            oauth_token_secret = access_token[b'oauth_token_secret'].decode("utf-8")
        else:
            return HttpResponseRedirect(reverse('mysocial-index'))
        try:
            user = User.objects.get(twitter_user_id=user_id)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='%s@twitter.com' % screen_name,
                password=user_id,
                twitter_screen_name=screen_name,
                twitter_oauth_token_secret=oauth_token_secret,
                twitter_oauth_token=oauth_token,
                twitter_user_id=user_id)
        user.twitter_oauth_token = oauth_token
        user.twitter_oauth_token_secret = oauth_token_secret
        user.save()
        user = authenticate(username='%s@twitter.com' % screen_name,
                            password=user_id)
        login(request, user)
        return HttpResponseRedirect(reverse('mysocial-twitter-home'))


class TwitterUserTimelineView(View):
    template_name = 'twitter_index.html'

    def get(self, request):
        # print(request)
        print(request.user)
        if request.user is not None:
            oauth_token = request.user.twitter_oauth_token
            oauth_token_secret = request.user.twitter_oauth_token_secret
            try:
                twitter = Twython(config('TWITTER_CONSUMER_KEY'),
                                  config('TWITTER_CONSUMER_SECRET'),
                                  oauth_token, oauth_token_secret)
                user_timeline = twitter.get_user_timeline()
                # print(home_timeline)
                data = user_timeline
                return render(request, self.template_name, {'data': data})
            except Exception:
                return HttpResponseRedirect(reverse('mysocial-twitter-home'))
        else:
            return HttpResponseRedirect(reverse('mysocial-index'))


class TwitterHomeView(View):
    template_name = 'twitter_index.html'

    def get(self, request):
        print(request.user)
        if request.user is not None:
            oauth_token = request.user.twitter_oauth_token
            oauth_token_secret = request.user.twitter_oauth_token_secret
            try:
                twitter = Twython(config('TWITTER_CONSUMER_KEY'),
                                  config('TWITTER_CONSUMER_SECRET'),
                                  oauth_token, oauth_token_secret)
                user_timeline = twitter.get_home_timeline()
                data = user_timeline
                return render(request, self.template_name, {'data': data})
            except Exception:
                return HttpResponseRedirect(reverse('mysocial-home'))
        else:
            return HttpResponseRedirect(reverse('mysocial-index'))


class TwitterFavListView(View):
    template_name = 'twitter_index.html'

    def get(self, request):
        # print(request)
        print(request.user)
        if request.user is not None:
            oauth_token = request.user.twitter_oauth_token
            oauth_token_secret = request.user.twitter_oauth_token_secret
            try:
                twitter = Twython(config('TWITTER_CONSUMER_KEY'),
                                  config('TWITTER_CONSUMER_SECRET'),
                                  oauth_token, oauth_token_secret)
                data = twitter.get_favorites()
                return render(request, self.template_name, {'data': data})
            except Exception:
                return HttpResponseRedirect(reverse('mysocial-twitter-home'))
        else:
            return HttpResponseRedirect(reverse('mysocial-index'))


@login_required
def my_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('mysocial-index'))


class InstaView(View):
    template_name = 'twitter_index.html'

    def get(self, request, *args, **kwargs):
        client_id = config('INSTA_CLIENT_ID')
        return redirect(
            INSTA_AUTHORIZE_URL + "?client_id=%s&redirect_uri=%s&response_type=code" % (
                client_id, INSTA_CALLBACK_URL))


class InstaCallbackView(View):
    template_name = 'insta_index.html'

    def get(self, request, *args, **kwargs):
        print(request)
        if 'error' in request.GET:
            print(request.GET.get('error_reason'), request.GET.get('error_description'))
            return HttpResponseRedirect(reverse('mysocial-home'))
        else:
            data = {
                'client_id': config('INSTA_CLIENT_ID'),
                'client_secret': config('INSTA_SECRET'),
                'grant_type': 'authorization_code',
                'redirect_uri': INSTA_CALLBACK_URL,
                'code': request.GET.get('code')

            }
            res = requests.post(INSTA_ACCESS_TOKEN_URL, data=data)
            json_response = json.loads(res.content.decode('utf-8'))
            access_token = json_response['access_token']
            print(access_token)
            user = json_response['user']
            # print(user)
            user_id = user['id']
            full_name = user['full_name']
            username = user['username']
            try:
                user = User.objects.get(twitter_user_id=user_id)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username='%s@instagram.com' % username,
                    password=user_id,
                    twitter_screen_name=full_name,
                    twitter_user_id=user_id,
                    twitter_oauth_token=access_token)
            user.twitter_oauth_token = access_token
            user.save()

            user = authenticate(username='%s@instagram.com' % username,
                                password=user_id)
            print(user)
            login(request, user)
            print(request.user)
            return HttpResponseRedirect(reverse('mysocial-insta-timeline'))


class InstaMediaView(View):
    template_name = 'insta_media.html'

    def get(self, request, media_id):
        # print(request)
        print(request.user)
        if 'error' in request.GET:
            print(request.GET.get('error_reason'), request.GET.get('error_description'))
            return HttpResponseRedirect(reverse('mysocial-insta-timeline'))
        else:
            access_token = request.user.twitter_oauth_token
            print(access_token)
            try:
                res = requests.get(
                    INSTA_COMMENTS_URL.format(media_id, access_token))

                print(res.content.decode('utf-8'))
                json_response = json.loads(res.content.decode('utf-8'))
                comments = json_response['data']
                res = requests.get(
                    INSTA_MEDIA_URL.format(media_id, access_token))

                print(res.content.decode('utf-8'))
                json_response = json.loads(res.content.decode('utf-8'))
                media = json_response['data']
                return render(request, self.template_name, {'comments': comments, 'media': media})
            except Exception:
                return HttpResponseRedirect(reverse('mysocial-insta-timeline'))


class InstaTimelineView(View):
    template_name = 'insta_index.html'

    def get(self, request):
        print(request.user)
        if 'error' in request.GET:
            print(request.GET.get('error_reason'), request.GET.get('error_description'))
            return HttpResponseRedirect(reverse('mysocial-insta-timeline'))
        else:
            access_token = request.user.twitter_oauth_token
            print(access_token)
            try:
                res = requests.get(
                    INSTA_TIMELINE_URL.format(
                        access_token, 20))

                # print(res.content.decode('utf-8'))
                json_response = json.loads(res.content.decode('utf-8'))
                data = json_response['data']
                # data = {}
                return render(request, self.template_name, {'data': data})
            except Exception:
                return HttpResponseRedirect(reverse('mysocial-home'))


class InstaLikedView(View):
    template_name = 'insta_index.html'

    def get(self, request):
        # print(request)
        print(request.user)
        if 'error' in request.GET:
            print(request.GET.get('error_reason'), request.GET.get('error_description'))
            return HttpResponseRedirect(reverse('mysocial-insta-timeline'))
        else:
            access_token = request.user.twitter_oauth_token
            print(access_token)
            try:
                res = requests.get(
                    INSTA_LIKED_URL.format(access_token))
                print(res.content.decode('utf-8'))
                json_response = json.loads(res.content.decode('utf-8'))

                data = json_response['data']
                # data = {}
                return render(request, self.template_name, {'data': data})
            except Exception:
                return HttpResponseRedirect(reverse('mysocial-insta-timeline'))
