from ..models import TwitterAuthToken, TwitterUser
from twitter_api.twitter_api import TwitterAPI

from datetime import datetime, timedelta

def run():
    users = TwitterUser.objects.all()
    for twitter_user in users:
        
        if twitter_user.minutes_rt == -1:
            continue
        
        end_time = (datetime.today() - timedelta(minutes= int(twitter_user.minutes_rt))).replace(microsecond=0).isoformat('T')+ "Z"
        # start_time = (datetime.today() - timedelta(minutes = int(100))).replace(microsecond=0).isoformat('T')+ "Z"

        twitter_api = TwitterAPI()
        tweets = twitter_api.get_users_retweets(twitter_user.twitter_id, end_time=end_time)

        twitter_api.unretweet(tweet_ids=tweets, access_token=twitter_user.twitter_oauth_token.oauth_token,access_token_secret=twitter_user.twitter_oauth_token.oauth_token_secret)
