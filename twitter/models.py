from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    text = models.CharField(max_length=140, null=False)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    about = models.TextField(max_length=140, null=False)
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followed_by')
    tweets = models.ManyToManyField(Tweet, through="TweetProfile")

class TweetProfile(models.Model):
    profile = models.ForeignKey(Profile)
    tweet = models.ForeignKey(Tweet)

class Comment(models.Model):
    text = models.CharField(max_length=140, null=False)
    user = models.ForeignKey(User)
    tweet = models.ForeignKey(Tweet)

class ProfilePhoto(models.Model):
    image_path = models.CharField(max_length=50)
    profile = models.OneToOneField(Profile, primary_key=True)

