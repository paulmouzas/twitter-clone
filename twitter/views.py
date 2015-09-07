from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, TweetForm, ProfileForm, AuthenticationForm
from .models import Tweet, User, Profile


def index(request):
    if request.user.is_authenticated():
        current_user = request.user
        tweets = current_user.profile.tweets.all()
        # don't include the current user in the users to follow list
        # or people you're already following
        people_not_to_follow = [p.pk for p in current_user.profile.follows.all()]
        people_not_to_follow.append(current_user.profile.pk)
        profiles_to_follow = Profile.objects.exclude(pk__in=people_not_to_follow)
        people_you_follow = current_user.profile.follows.all()
        your_followers = request.user.profile.followed_by.all()

        if request.method == 'GET':
            tweet_form = TweetForm()
            context = {
                'tweet_form': tweet_form,
                'tweets': tweets,
                'profiles_to_follow': profiles_to_follow,
                'your_followers': your_followers,
                'people_you_follow': people_you_follow,
            }
            return render(request, 'index.html', context=context)

        elif request.method == 'POST':
            tweet_form = TweetForm(request.POST)
            if tweet_form.is_valid():
                text = tweet_form.cleaned_data['text']
                tweet_form.save(user=request.user, text=text)
                return redirect('index')
            else:
                return render(request, 'index.html', 
                        context={'tweet_form': tweet_form, 'tweets': tweets})
    # user's not authenticated so go to signup
    return redirect('signup')


def signup(request):
    if request.method == 'POST':
        signup_form = MyUserCreationForm(request.POST)
        if signup_form.is_valid():
            new_user = signup_form.save()
            # create a new profiel for the new user
            profile = Profile(user=new_user, about="No about yet")
            profile.save()
            username = signup_form.cleaned_data['username']
            password = signup_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            # TODO create profile before redirecting to index
            return redirect('index')
        return render(request, 'signup.html',
                context={'signup_form': signup_form})
    elif request.method == 'GET':
        signup_form = MyUserCreationForm()
        return render(request, 'signup.html',
                context={'signup_form': signup_form})

def profile(request, username):
    if request.method == 'GET':
        user = User.objects.get(username=username)
        context = {'user': user}
        return render(request, 'profile.html', context=context)

def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            about = profile_form.cleaned_data['about']
            profile_form.save(about=about, user=user)
            username = user.username
            return redirect('profile', username=username)

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'user': user}
        return render(request, 'profile_form.html', context=context)

def delete_tweet(request, tweet_id):
    # check if this tweet belongs to the logged in user
    print tweet_id
    if request.method == 'POST':
        tweet = Tweet.objects.get(pk=tweet_id)
        if request.user == tweet.user:
            tweet.delete()
        else:
            print 'nope'
        return redirect('index')

def signout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

def follow(request, profile_id):
    if request.method == 'POST':
        profile = Profile.objects.get(pk=profile_id)
        request.user.profile.follows.add(profile)
        return redirect('index')

def signin(request):
    if request.method == 'GET':
        signin_form = AuthenticationForm()
        context = {'signin_form': signin_form}
        return render(request, 'signin.html', context=context)
    elif request.method == 'POST':
        signin_form = AuthenticationForm(data=request.POST)
        if signin_form.is_valid():
            login(request, signin_form.get_user())
            return redirect('index')
        else:
            context = {'signin_form': signin_form}
            return render(request, 'signin.html', context=context)
