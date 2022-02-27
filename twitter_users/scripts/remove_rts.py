from ..models import TwitterAuthToken, TwitterUser
from twitter_api.twitter_api import TwitterAPI
from django.utils import timezone

from datetime import datetime, timedelta

def run():
    users = TwitterUser.objects.all()
    for twitter_user in users:
        
        if twitter_user.minutes_rt == -1:
            continue

        start_time = None
        if twitter_user.last_rm_rt_check:
            last_check = datetime.strptime(datetime.strftime(twitter_user.last_rm_rt_check, "%d-%m-%Y %H:%M:%S"), "%d-%m-%Y %H:%M:%S")
            start_time = last_check.isoformat('T')+ "Z"

        end_time = (datetime.now() - timedelta(minutes= int(twitter_user.minutes_rt))).replace(microsecond=0).isoformat('T')+ "Z"

        if start_time and start_time >= end_time:
            continue
        
        twitter_api = TwitterAPI()
        tweets = twitter_api.get_users_retweets(twitter_user.twitter_id, end_time=end_time, start_time= start_time)
        
        if len(tweets) > 0:
            twitter_api.unretweet(tweet_ids=tweets, access_token=twitter_user.twitter_oauth_token.oauth_token,access_token_secret=twitter_user.twitter_oauth_token.oauth_token_secret)
        
        twitter_user.last_rm_rt_check = datetime.now(tz=timezone.utc)
        twitter_user.save()
