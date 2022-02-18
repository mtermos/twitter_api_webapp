import tweepy
from decouple import config


class TwitterAPI:
    def __init__(self):
        self.api_key = config('TWITTER_API_KEY')
        self.api_secret = config('TWITTER_API_SECRET')
        self.client_id = config('TWITTER_CLIENT_ID')
        self.client_secret = config('TWITTER_CLIENT_SECRET')
        self.access_token = config('TWITTER_ACCESS_TOKEN')
        self.access_secret = config('TWITTER_ACCESS_SECRET')
        self.oauth_callback_url = config('TWITTER_OAUTH_CALLBACK_URL')
        self.bearer_token = config('TWITTER_BEARER_TOKEN')

    def twitter_login(self):
        oauth1_user_handler = tweepy.OAuth1UserHandler(self.api_key, self.api_secret, callback=self.oauth_callback_url)
        url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)
        request_token = oauth1_user_handler.request_token["oauth_token"]
        request_secret = oauth1_user_handler.request_token["oauth_token_secret"]
        return url, request_token, request_secret

    def twitter_callback(self,oauth_verifier, oauth_token, oauth_token_secret):
        oauth1_user_handler = tweepy.OAuth1UserHandler(self.api_key, self.api_secret, callback=self.oauth_callback_url)
        oauth1_user_handler.request_token = {
            'oauth_token': oauth_token,
            'oauth_token_secret': oauth_token_secret
        }
        access_token, access_token_secret = oauth1_user_handler.get_access_token(oauth_verifier)
        return access_token, access_token_secret

    def get_me(self, access_token, access_token_secret):
        try:
            client = tweepy.Client(consumer_key=self.api_key, consumer_secret=self.api_secret, access_token=access_token,
                                   access_token_secret=access_token_secret)

            info = client.get_me(user_auth=True, expansions='pinned_tweet_id')
            return info
        except Exception as e:
            print(e)
            return None

    def get_users_retweets(self, twitter_id, end_time, start_time = None):
        try:
            client = tweepy.Client(
                bearer_token = self.bearer_token,
                consumer_key = self.api_key,
                consumer_secret = self.api_secret,
            )

            tweet_fields=["referenced_tweets"]

            user_tweets = tweepy.Paginator(client.get_users_tweets,
                id = twitter_id,
                end_time = end_time,
                start_time = start_time,
                tweet_fields = tweet_fields
            )

            tweets = []
            for page in user_tweets:
                if page.data:
                    for tweet in page.data:
                        if tweet.referenced_tweets is not None and tweet.referenced_tweets[0].data["type"] == "retweeted":
                            tweets.append(tweet.id)
            return tweets

        except Exception as e:
            print(e)
            return None


    def unretweet(self,tweet_ids ,access_token,access_token_secret):
        try:
            auth = tweepy.OAuth1UserHandler(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                # access_token=self.access_token,
                # access_token_secret=self.access_secret,
            )

            api = tweepy.API(auth)

            for id in tweet_ids:
                api.unretweet(id)
                
            # api.unretweet(1469583239090159622)
            # api.unretweet(1469587591938854913)
            # api.unretweet(1493861421024788482)
            # api.unretweet(1493938292080926727)

            # client = tweepy.Client(
            #     bearer_token = self.bearer_token,
            #     consumer_key= self.api_key,
            #     consumer_secret= self.api_secret,
            #     # access_token=self.access_token,
            #     # access_token_secret=self.access_secret,
            #     access_token=access_token,
            #     access_token_secret=access_token_secret,
            # )


            # print("========")
            # client.unretweet(1493940398036770820, user_auth= True)
            # client.unretweet(1493938292080926727)



        except Exception as e:
            print(e)
            return None

    def get_user_timeline(self, twitter_id, end_time, start_time = None):
        try:

            auth = tweepy.OAuth1UserHandler(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=None,
                access_token_secret=None
            )
            api = tweepy.API(auth)
            timeline = api.user_timeline(user_id = twitter_id, include_rts = True)
            # for message in api.user_timeline(user_id = twitter_id, include_rts = True):
            #     print("========>>>>>>", message)
            print("========>>>>>>", timeline)

            return timeline
        except Exception as e:
            print(e)
            return None
