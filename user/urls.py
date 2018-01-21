from django.urls import path

from .views import *

urlpatterns = [

    path('index/', LoginView.as_view(), name='mysocial-index'),
    path('logout/', my_logout, name='mysocial-logout'),
    path('home/', HomeView.as_view(), name='mysocial-home'),
    path('twitter/', TwitterView.as_view(), name='mysocial-twitter'),
    path('twitter_callback/', TwitterCallbackView.as_view(), name='mysocial-twitter-callback'),
    path('twitter_user_timeline/', TwitterUserTimelineView.as_view(), name='mysocial-twitter-user-timeline'),
    path('twitter_home/', TwitterHomeView.as_view(), name='mysocial-twitter-home'),
    path('twitter_fav_list/', TwitterFavListView.as_view(), name='mysocial-twitter-fav-list'),
    path('instagram/', InstaView.as_view(), name='mysocial-insta'),
    path('insta_callback/', InstaCallbackView.as_view(), name='mysocial-insta-callback'),
    path('insta_timeline/', InstaTimelineView.as_view(), name='mysocial-insta-timeline'),
    path('instagram/media/<str:media_id>/', InstaMediaView.as_view(), name='mysocial-insta-media'),
    path('insta_liked/', InstaLikedView.as_view(), name='mysocial-insta-liked'),

]