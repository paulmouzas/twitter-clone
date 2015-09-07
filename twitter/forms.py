from django import forms
from django.forms.models import ModelForm
from .models import User, Tweet, Profile, TweetProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.html import strip_tags
from django.core.exceptions import ObjectDoesNotExist


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))

    def is_valid(self):
        form = super(MyUserCreationForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all_':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

    class Meta:
        fields = ['email', 'username', 'first_name', 'last_name', 'password1',
                  'password2']
        model = User

class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ('text',)
    def save(self, **kwargs):
        text = kwargs['text']
        user = kwargs['user']
        tweet = Tweet(text=text, user=user)
        tweet.save()

        # add this tweet to the original users profile
        tp = TweetProfile(profile=user.profile, tweet=tweet)
        tp.save()

        #add this tweet to all the followers profiles
        followers = user.profile.followed_by.all()
        for follower in followers:
            tp = TweetProfile(profile=follower, tweet=tweet)
            tp.save()

        # add this tweet to any one on it was directed to
        words = text.split()
        for word in words:
            if word.startswith('@'):
                try:
                    at_user = User.objects.get(username=word[1:])
                    tp = TweetProfile(profile=at_user.profile, tweet=tweet)
                    tp.save()
                except ObjectDoesNotExist:
                    pass
        return tweet

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('about',)
    def save(self, **kwargs):
        about = kwargs['about']
        user = kwargs['user']
        profile = Profile(about=about, user=user)
        profile.save()
        return profile
