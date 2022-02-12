from django.shortcuts import render
import tweepy

# Create your views here.


access_token = "1299812125968338949-dlBP1pc8IogL1gOwHFhxyTSBWh8qsX"
access_token_secret = "41iSq83eBAT4bt9xYGQsphKBlHMPZqHt7OTNHUWAz4Ui7"

consumer_key = "dYP1FzJMwk2jSreLMw2J4UeOi"
consumer_secret = "AAy61x9S530jmYvWE47yZXVVk5fKVB2kcgFS7kxPqkZfz0s3OW"

def home(request):

    oauth1_user_handler = tweepy.OAuth1UserHandler(
        consumer_key= consumer_key, consumer_secret= consumer_secret,
        callback= "http://localhost:8000/first_demo/"
    )
    print(oauth1_user_handler.get_authorization_url())

    return render(request, 'home.html')