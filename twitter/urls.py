from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^signout/', views.signout, name='signout'),
    url(r'^signin/', views.signin, name='signin'),
    url(r'^profile/(?P<username>[a-z0-9]{3,16})/', views.profile, name='profile'),
    url(r'^edit_profile/', views.edit_profile, name='edit_profile'),
    url(r'^delete_tweet/(?P<tweet_id>[0-9]+)/', views.delete_tweet, name='delete_tweet'),
    url(r'^follow/(?P<profile_id>[0-9]+)/', views.follow, name='follow'),
]
