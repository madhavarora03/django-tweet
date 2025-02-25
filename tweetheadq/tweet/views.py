from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TweetForm, UserRegisterForm
from .models import Tweet


# Create your views here.
def index(request):
    return render(request, 'index.html')


def list_all_tweets(request):
    tweets = Tweet.objects.all().order_by('-created_at')

    return render(request, 'tweet_list.html', {'tweets': tweets})


@login_required
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)

        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('list_all_tweets')
    else:
        form = TweetForm()

    return render(request, 'tweet_form.html', {'form': form})


@login_required
def edit_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)

        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('list_all_tweets')
    else:
        form = TweetForm(instance=tweet)

    return render(request, 'tweet_form.html', {'form': form})


@login_required
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        tweet.delete()
        return redirect('list_all_tweets')

    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('list_all_tweets')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})