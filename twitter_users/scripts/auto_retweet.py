from ..models import AutoRetweetRecords, TwitterAuthToken, TwitterUser
from twitter_api.twitter_api import TwitterAPI
from django.utils import timezone

from datetime import datetime, timedelta

def run():
    users = TwitterUser.objects.all()
    for twitter_user in users:
        
        if twitter_user.hours_auto_rt == -1 or not twitter_user.last_auto_rt_check:
            continue

        start_time = datetime.strptime(datetime.strftime(twitter_user.last_auto_rt_check, "%d-%m-%Y %H:%M:%S"), "%d-%m-%Y %H:%M:%S")
        end_time = datetime.strptime(datetime.strftime(datetime.now(tz=timezone.utc) - timedelta(hours= int(twitter_user.hours_auto_rt)), "%d-%m-%Y %H:%M:%S"), "%d-%m-%Y %H:%M:%S")
        
        if start_time and start_time >= end_time:
            continue

        start_time.isoformat('T')+ "Z"
        end_time.isoformat('T')+ "Z"

        twitter_api = TwitterAPI()
        tweets = twitter_api.get_users_tweets(twitter_user.twitter_id, end_time=end_time, start_time= start_time)
        
        if not tweets:
            continue
        
        if len(tweets) > 0:
            twitter_api.retweet(tweet_ids=tweets, access_token=twitter_user.twitter_oauth_token.oauth_token,access_token_secret=twitter_user.twitter_oauth_token.oauth_token_secret)
        
        for id in tweets:
            record = AutoRetweetRecords(
                tweet_id = id,
                user = twitter_user
            )
            record.save()

        twitter_user.last_auto_rt_check = datetime.now(tz=timezone.utc)
        twitter_user.auto_rts_count += len(tweets)
        twitter_user.save()

        
