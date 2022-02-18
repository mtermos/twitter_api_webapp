from functools import wraps
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from twitter_users.authorization import check_token_still_valid
from twitter_users.models import TwitterUser


def twitter_login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        twitter_user = TwitterUser.objects.filter(user=request.user).first()
        info = check_token_still_valid(twitter_user)
        if info is None:
            logout(request)
            return HttpResponseRedirect(reverse('twitter_login'))
        else:
            request.twitter_user = twitter_user
            return function(request, *args, **kwargs)
    return wrap