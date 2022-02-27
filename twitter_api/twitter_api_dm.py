import json
import tweepy
from decouple import config
from tweepy.parsers import ModelParser, Parser
from .custom_models import CustomModelFactory


class TwitterAPIDM:
    def __init__(self):

        self.api_key = config('DM_TWITTER_API_KEY')
        self.api_secret = config('DM_TWITTER_API_SECRET')
        self.client_id = config('DM_TWITTER_CLIENT_ID')
        self.client_secret = config('DM_TWITTER_CLIENT_SECRET')
        self.access_token = config('DM_TWITTER_ACCESS_TOKEN')
        self.access_secret = config('DM_TWITTER_ACCESS_SECRET')
        self.oauth_callback_url = config('DM_TWITTER_OAUTH_CALLBACK_URL')
        self.bearer_token = config('DM_TWITTER_BEARER_TOKEN')

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




    def add_welcome_message(self, access_token, access_token_secret,text, name=None,
        quick_reply_options=None,attachment_type=None, attachment_media_id=None, ctas=None,):
        try:
            auth = tweepy.OAuth1UserHandler(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )

            api = tweepy.API(auth)

            json_payload = {
                'welcome_message': {
                    'name': name,
                    'message_data': {'text': text}
                }
            }

            message_data = json_payload['welcome_message']['message_data']
            if quick_reply_options is not None:
                message_data['quick_reply'] = {
                    'type': 'options',
                    'options': quick_reply_options
                }
            if attachment_type is not None and attachment_media_id is not None:
                message_data['attachment'] = {
                    'type': attachment_type,
                    'media': {'id': attachment_media_id}
                }
            if ctas is not None:
                message_data['ctas'] = ctas

            api.request(
                'POST', 'direct_messages/welcome_messages/new',
                json_payload=json_payload
            )


        except Exception as e:
            print(e)
            return None

    def get_welcome_messages_list(self, access_token, access_token_secret):
        try:
            auth = tweepy.OAuth1UserHandler(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )

            api = tweepy.API(auth)

            welcome_parser = ModelParser(model_factory=CustomModelFactory)
            response = api.request(
                'GET', 'direct_messages/welcome_messages/list',
                payload_type="welcome_message",
                parser=welcome_parser,
                payload_list = True
            )

            return response


        except Exception as e:
            print(e)
            return None

    def get_welcome_message(self, access_token, access_token_secret, id):
        try:
            auth = tweepy.OAuth1UserHandler(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )

            api = tweepy.API(auth)
            endpoint_parameters=('id')

            welcome_parser = ModelParser(model_factory=CustomModelFactory)
            response = api.request(
                'GET', 'direct_messages/welcome_messages/show',
                endpoint_parameters=endpoint_parameters,
                id=id,
                payload_type="welcome_message",
                parser=welcome_parser
            )
            print("======>>>>>>> get_welcome_message: ", type(response))
            return response


        except Exception as e:
            print(e)
            return None

    def delete_welcome_message(self, access_token, access_token_secret, id):
        try:
            auth = tweepy.OAuth1UserHandler(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )

            api = tweepy.API(auth)

            response = api.request(
                'DELETE', 'direct_messages/welcome_messages/destroy',
                endpoint_parameters=('id'),
                id=id
            )

            return response


        except Exception as e:
            print(e)
            return None

    def update_welcome_message(self, access_token, access_token_secret, id, name,text,
        quick_reply_options=None,attachment_type=None, attachment_media_id=None, ctas=None):
        try:
            auth = tweepy.OAuth1UserHandler(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )

            api = tweepy.API(auth)

            json_payload = {
                    'name': name,
                    'message_data': {'text': text}
            }

            message_data = json_payload['message_data']
            if quick_reply_options is not None:
                message_data['quick_reply'] = {
                    'type': 'options',
                    'options': quick_reply_options
                }
            if attachment_type is not None and attachment_media_id is not None:
                message_data['attachment'] = {
                    'type': attachment_type,
                    'media': {'id': attachment_media_id}
                }
            if ctas is not None:
                message_data['ctas'] = ctas

            response = api.request(
                'PUT', 'direct_messages/welcome_messages/update',
                endpoint_parameters=('id'),
                id=id,
                json_payload=json_payload
            )

            return response


        except Exception as e:
            print(e)
            return None





    def get_rules_list(self, api= None,access_token = None, access_token_secret=None):
        try:

            if api is None:
                auth = tweepy.OAuth1UserHandler(
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=access_token,
                    access_token_secret=access_token_secret,
                )

                api = tweepy.API(auth)

            welcome_parser = ModelParser(model_factory=CustomModelFactory)
            response = api.request(
                'GET', 'direct_messages/welcome_messages/rules/list',
                payload_type="rule",
                parser=welcome_parser,
                payload_list = True
            )

            return response


        except Exception as e:
            print(e)
            return None

    def get_rule(self, access_token, access_token_secret, id):
        try:
            auth = tweepy.OAuth1UserHandler(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )

            api = tweepy.API(auth)
            endpoint_parameters=('id')

            welcome_parser = ModelParser(model_factory=CustomModelFactory)
            response = api.request(
                'GET', 'direct_messages/welcome_messages/rules/show',
                endpoint_parameters=endpoint_parameters,
                id=id,
                payload_type="rule",
                parser=welcome_parser
            )

            return response


        except Exception as e:
            print(e)
            return None

    def add_rule(self, access_token, access_token_secret, welcome_message_id):

        try:
            auth = tweepy.OAuth1UserHandler(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )

            api = tweepy.API(auth)

            existing_rules = self.get_rules_list(api=api)

            if len(existing_rules) > 0:
                self.delete_rule(id=existing_rules[0].id, api=api)

            json_payload = {
                'welcome_message_rule': {
                    'welcome_message_id': welcome_message_id
                }
            }
            response = api.request(
                'POST', 'direct_messages/welcome_messages/rules/new',
                json_payload=json_payload
            )

            return response


        except Exception as e:
            print(e)
            return None
   
    def delete_rule(self, id, api = None, access_token = None, access_token_secret = None, ):

        try:
            if api is None:
                auth = tweepy.OAuth1UserHandler(
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=access_token,
                    access_token_secret=access_token_secret,
                )

                api = tweepy.API(auth)

            response = api.request(
                'DELETE', 'direct_messages/welcome_messages/rules/destroy',
                endpoint_parameters=('id'),
                id=id
            )

            return response


        except Exception as e:
            print(e)
            return None

