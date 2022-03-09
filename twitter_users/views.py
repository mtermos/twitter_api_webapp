# from distutils.command.config import config

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from twitter_api.custom_models import WelcomeMessage

import twitter_users
from .decorators import twitter_login_required, twitter_dm_login_required
from .models import TwitterAuthToken, TwitterDMAuthToken, TwitterUser
from .authorization import create_update_user_from_twitter, create_update_user_from_twitter_dm, check_token_still_valid
from twitter_api.twitter_api import TwitterAPI
from twitter_api.twitter_api_dm import TwitterAPIDM
from decouple import config
from datetime import datetime, timedelta



def index(request):

    context = {}
    
    if request.user.is_authenticated:
        twitter_user = TwitterUser.objects.filter(user=request.user).first()

        if twitter_user:
            context["minutes_rt"] = twitter_user.minutes_rt

            if twitter_user.twitter_oauth_token:
                context["rm_rt_access"] = True

                context["minutes_rm_rt"] = twitter_user.minutes_rt
                context["removed_rts_count"] = twitter_user.removed_rts_count

                context["hours_auto_rt"] = twitter_user.hours_auto_rt
                context["auto_rts_count"] = twitter_user.auto_rts_count

            if twitter_user.twitter_dm_oauth_token:
                context["dm_access"] = True
                

    return render(request, 'twitter_users/index.html', context=context)


@twitter_login_required
def dashboards(request):

    context = {}
    if request.user.is_authenticated and hasattr(request, "twitter_user"):
        context["twitter_user"] = request.twitter_user

    return render(request, 'twitter_users/dashboards.html', context=context)


def login_page(request):

    context = {}
    if request.user.is_authenticated:
        twitter_user = TwitterUser.objects.filter(user=request.user).first()
        context["minutes_rt"] = twitter_user.minutes_rt

        if twitter_user.twitter_oauth_token:
            context["rm_rt_access"] = True

        if twitter_user.twitter_dm_oauth_token:
            context["dm_access"] = True
    
    return render(request, 'twitter_users/login.html', context=context)




@login_required
def twitter_logout(request):
    logout(request)
    return redirect('index')


@login_required
@twitter_login_required
def remove_retweets_create_page(request):
    user_minutes = request.twitter_user.minutes_rt
    if user_minutes >= 0:
        context = {
            'minutes_rt' : user_minutes,
            'is_active' : True,
        }
    else:
        context = {
            'minutes_rt' : 0,
            'is_active' : False,
        }
    return render(request, 'twitter_users/remove_retweets.html', context= context)


@login_required
@twitter_login_required
def remove_retweets_create(request):
    
    if request.POST.get("active"):
        request.twitter_user.minutes_rt = request.POST.get("minutes_num")
    else:
        request.twitter_user.minutes_rt = -1

    request.twitter_user.save()
    return redirect('index')



@login_required
@twitter_dm_login_required
def welcome_message_create_page(request):

    api = TwitterAPIDM()
    welcome_message = api.get_welcome_messages_list(
        access_token=request.twitter_user.twitter_dm_oauth_token.oauth_token,
        access_token_secret= request.twitter_user.twitter_dm_oauth_token.oauth_token_secret,
    )

    wlc_rules = api.get_rules_list(
        access_token=request.twitter_user.twitter_dm_oauth_token.oauth_token,
        access_token_secret= request.twitter_user.twitter_dm_oauth_token.oauth_token_secret,
    )

    if wlc_rules and len(wlc_rules) > 0 and wlc_rules[0] is not None:
        rule = wlc_rules[0]
        default_id = rule.welcome_message_id
    else:
        default_id = -1

    messages_json = []

    if welcome_message:
        for message in welcome_message:
            text = message.message_data["text"]
            if "رسالة الترحيب بواسطة" in text.splitlines()[-1]:
                text = text[:text.rfind('\n')]

            messages_json.append({"id":message.id, "name" : message.name, "text":text})

    if welcome_message is not None:
        context = {
            'messages_json' : messages_json,
            'default_id' : default_id,
            'is_set' : True
        }
    else:
        context = {
            'is_set' : False
        }

    return render(request, 'twitter_users/welcome_message.html', context= context)


@login_required
@twitter_dm_login_required
def welcome_message_create(request):
    
    text = request.POST.get("text") + "\n" + "رسالة الترحيب بواسطة: adawat.tech"
    api = TwitterAPIDM()
    created_message = api.add_welcome_message(
        access_token=request.twitter_user.twitter_dm_oauth_token.oauth_token,
        access_token_secret= request.twitter_user.twitter_dm_oauth_token.oauth_token_secret,
        text = text,
        name = request.POST.get("name"),
    )
    return redirect('welcome_message_create_page')

@login_required
@twitter_dm_login_required
def welcome_message_delete(request, id):
    api = TwitterAPIDM()
    is_deleted = api.delete_welcome_message(
        access_token=request.twitter_user.twitter_dm_oauth_token.oauth_token,
        access_token_secret= request.twitter_user.twitter_dm_oauth_token.oauth_token_secret,
        id = id
    )

    return redirect('welcome_message_create_page')

@login_required
@twitter_dm_login_required
def make_welcome_message_default(request):
    api = TwitterAPIDM()
    rule = api.add_rule(
        access_token=request.twitter_user.twitter_dm_oauth_token.oauth_token,
        access_token_secret= request.twitter_user.twitter_dm_oauth_token.oauth_token_secret,
        welcome_message_id = request.POST.get("id")
    )

    return redirect('welcome_message_create_page')

@login_required
@twitter_dm_login_required
def welcome_message_edit(request, id):

    if not id:
        return redirect("welcome_message_create_page")

    api = TwitterAPIDM()
    message = api.get_welcome_message(
        access_token=request.twitter_user.twitter_dm_oauth_token.oauth_token,
        access_token_secret= request.twitter_user.twitter_dm_oauth_token.oauth_token_secret,
        id = id
    )

    text = message.message_data["text"]
    if "رسالة الترحيب بواسطة" in text.splitlines()[-1]:
        message.message_data["text"] = text[:text.rfind('\n')]

    if message:
        context = {
            'message' : message,
        }
    else:
        return redirect("welcome_message_create_page")

    return render(request, 'twitter_users/welcome_message_edit.html', context= context)



@login_required
@twitter_dm_login_required
def welcome_message_update(request):
    text = request.POST.get("text") + "\n" + "رسالة الترحيب بواسطة: adawat.tech"

    api = TwitterAPIDM()
    update_message = api.update_welcome_message(
        access_token =request.twitter_user.twitter_dm_oauth_token.oauth_token,
        access_token_secret = request.twitter_user.twitter_dm_oauth_token.oauth_token_secret,
        id = request.POST.get("id"),
        text = text,
        name = request.POST.get("name"),
    )
    return redirect('welcome_message_create_page')



@login_required
@twitter_login_required
def auto_retweet_create(request):

    hours_auto_rt = request.twitter_user.hours_auto_rt
    if hours_auto_rt >= 0:
        context = {
            'hours_auto_rt' : hours_auto_rt,
            'is_active' : True,
        }
    else:
        context = {
            'hours_auto_rt' : 0,
            'is_active' : False,
        }
    
    if request.user_agent.is_mobile:
        return render(request, 'twitter_users/mobile/auto_retweet.html', context= context)

    return render(request, 'twitter_users/auto_retweet.html', context= context)


@login_required
@twitter_login_required
def auto_retweet_store(request):
    
    if request.POST.get("active"):
        request.twitter_user.hours_auto_rt = request.POST.get("hours_auto_rt")
    else:
        request.twitter_user.hours_auto_rt = -1

    request.twitter_user.save()
    return redirect('index')





# Create your views here.
def twitter_rm_rt_login(request):
    twitter_api = TwitterAPI()
    url, oauth_token, oauth_token_secret = twitter_api.twitter_login()
    if url is None or url == '':
        messages.add_message(request, messages.ERROR, 'Unable to login. Please try again.')
        return render(request, 'twitter_users/error_page.html')
    else:
        twitter_auth_token = TwitterAuthToken.objects.filter(oauth_token=oauth_token).first()
        if twitter_auth_token is None:
            twitter_auth_token = TwitterAuthToken(oauth_token=oauth_token, oauth_token_secret=oauth_token_secret)
            twitter_auth_token.save()
        else:
            twitter_auth_token.oauth_token_secret = oauth_token_secret
            twitter_auth_token.save()
        return redirect(url)


def twitter_rm_rt_callback(request):
    if 'denied' in request.GET:
        messages.add_message(request, messages.ERROR, 'Unable to login or login canceled. Please try again.')
        return render(request, 'twitter_users/error_page.html')
    twitter_api = TwitterAPI()
    oauth_verifier = request.GET.get('oauth_verifier')
    oauth_token = request.GET.get('oauth_token')
    twitter_auth_token = TwitterAuthToken.objects.filter(oauth_token=oauth_token).first()
    if twitter_auth_token is not None:
        access_token, access_token_secret = twitter_api.twitter_callback(oauth_verifier, oauth_token, twitter_auth_token.oauth_token_secret)
        if access_token is not None and access_token_secret is not None:
            twitter_auth_token.oauth_token = access_token
            twitter_auth_token.oauth_token_secret = access_token_secret
            twitter_auth_token.save()
            # Create user
            info = twitter_api.get_me(access_token, access_token_secret)
            if info is not None:
                twitter_user_new = TwitterUser(twitter_id=info[0]['id'], screen_name=info[0]['username'],
                                               name=info[0]['name'], profile_image_url=info[0]['profile_image_url'])
                twitter_user_new.twitter_oauth_token = twitter_auth_token
                user, twitter_user = create_update_user_from_twitter(twitter_user_new)
                if user is not None:
                    login(request, user)
                    return redirect("index")
            else:
                messages.add_message(request, messages.ERROR, 'Unable to get profile details. Please try again.')
                return render(request, 'twitter_users/error_page.html')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to get access token. Please try again.')
            return render(request, 'twitter_users/error_page.html')
    else:
        messages.add_message(request, messages.ERROR, 'Unable to retrieve access token. Please try again.')
        return render(request, 'twitter_users/error_page.html')



def twitter_dm_login(request):
    twitter_api = TwitterAPIDM()
    url, oauth_token, oauth_token_secret = twitter_api.twitter_login()
    if url is None or url == '':
        messages.add_message(request, messages.ERROR, 'Unable to login. Please try again.')
        return render(request, 'twitter_users/error_page.html')
    else:
        twitter_auth_token = TwitterDMAuthToken.objects.filter(oauth_token=oauth_token).first()
        if twitter_auth_token is None:
            twitter_auth_token = TwitterDMAuthToken(oauth_token=oauth_token, oauth_token_secret=oauth_token_secret)
            twitter_auth_token.save()
        else:
            twitter_auth_token.oauth_token_secret = oauth_token_secret
            twitter_auth_token.save()
        return redirect(url)


def twitter_dm_callback(request):
    if 'denied' in request.GET:
        messages.add_message(request, messages.ERROR, 'Unable to login or login canceled. Please try again.')
        return render(request, 'twitter_users/error_page.html')
    twitter_api = TwitterAPIDM()
    oauth_verifier = request.GET.get('oauth_verifier')
    oauth_token = request.GET.get('oauth_token')
    twitter_auth_token = TwitterDMAuthToken.objects.filter(oauth_token=oauth_token).first()
    if twitter_auth_token is not None:
        access_token, access_token_secret = twitter_api.twitter_callback(oauth_verifier, oauth_token, twitter_auth_token.oauth_token_secret)
        if access_token is not None and access_token_secret is not None:
            twitter_auth_token.oauth_token = access_token
            twitter_auth_token.oauth_token_secret = access_token_secret
            twitter_auth_token.save()
            # Create user
            info = twitter_api.get_me(access_token, access_token_secret)
            if info is not None:
                twitter_user_new = TwitterUser(twitter_id=info[0]['id'], screen_name=info[0]['username'],
                                               name=info[0]['name'], profile_image_url=info[0]['profile_image_url'])
                twitter_user_new.twitter_dm_oauth_token = twitter_auth_token
                user, twitter_user = create_update_user_from_twitter_dm(twitter_user_new)
                if user is not None:
                    login(request, user)
                    return redirect("index")
            else:
                messages.add_message(request, messages.ERROR, 'Unable to get profile details. Please try again.')
                return render(request, 'twitter_users/error_page.html')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to get access token. Please try again.')
            return render(request, 'twitter_users/error_page.html')
    else:
        messages.add_message(request, messages.ERROR, 'Unable to retrieve access token. Please try again.')
        return render(request, 'twitter_users/error_page.html')



