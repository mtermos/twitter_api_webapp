from ..models import RemoveRetweetsRecords, TwitterAuthToken, TwitterUser
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
            start_time = datetime.strptime(datetime.strftime(twitter_user.last_rm_rt_check, "%d-%m-%Y %H:%M:%S"), "%d-%m-%Y %H:%M:%S")

        end_time = (datetime.now(tz=timezone.utc) - timedelta(minutes= int(twitter_user.minutes_rt)))
        end_time = datetime.strptime(datetime.strftime(end_time, "%d-%m-%Y %H:%M:%S"), "%d-%m-%Y %H:%M:%S")
        


        if start_time and start_time >= end_time:
            continue

        start_time = start_time.isoformat('T')+ "Z"
        end_time = end_time.isoformat('T')+ "Z"

        
        twitter_api = TwitterAPI()
        tweets = twitter_api.get_users_retweets(twitter_user.twitter_id, end_time=end_time, start_time= start_time)
        
        if not tweets:
            continue

        if len(tweets) > 0:
            twitter_api.unretweet(tweet_ids=tweets, access_token=twitter_user.twitter_oauth_token.oauth_token,access_token_secret=twitter_user.twitter_oauth_token.oauth_token_secret)
        
        for id in tweets:
            record = RemoveRetweetsRecords(
                tweet_id = id,
                user = twitter_user
            )
            record.save()

        twitter_user.last_rm_rt_check = datetime.now(tz=timezone.utc)
        twitter_user.removed_rts_count += len(tweets)
        twitter_user.save()
