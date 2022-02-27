# Tweepy
# Copyright 2009-2022 Joshua Roesslein
# See LICENSE for details.

from email.utils import parsedate_to_datetime

from tweepy.mixins import HashableID

class Model:

    def __init__(self, api=None):
        self._api = api

    def __getstate__(self):
        pickle = self.__dict__.copy()
        pickle.pop('_api', None)
        return pickle

    @classmethod
    def parse(cls, api, json):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError

    @classmethod
    def parse_list(cls, api, json_list):
        """
            Parse a list of JSON objects into
            a result set of model instances.
        """
        results = ResultSet()

        if isinstance(json_list, dict):
            # Handle map parameter for statuses/lookup
            if 'id' in json_list:
                for _id, obj in json_list['id'].items():
                    if obj:
                        results.append(cls.parse(api, obj))
                    else:
                        results.append(cls.parse(api, {'id': int(_id)}))
                return results
            # Handle premium search
            if 'results' in json_list:
                json_list = json_list['results']

        for obj in json_list:
            if obj:
                results.append(cls.parse(api, obj))
        return results

    def __repr__(self):
        state = [f'{k}={v!r}' for (k, v) in vars(self).items()]
        return f'{self.__class__.__name__}({", ".join(state)})'


class ResultSet(list):
    """A list like object that holds results from a Twitter API query."""

    def __init__(self, max_id=None, since_id=None):
        super().__init__()
        self._max_id = max_id
        self._since_id = since_id

    @property
    def max_id(self):
        if self._max_id:
            return self._max_id
        ids = self.ids()
        # Max_id is always set to the *smallest* id, minus one, in the set
        return (min(ids) - 1) if ids else None

    @property
    def since_id(self):
        if self._since_id:
            return self._since_id
        ids = self.ids()
        # Since_id is always set to the *greatest* id in the set
        return max(ids) if ids else None

    def ids(self):
        return [item.id for item in self if hasattr(item, 'id')]

class Media(Model):

    @classmethod
    def parse(cls, api, json):
        media = cls(api)
        for k, v in json.items():
            setattr(media, k, v)
        return media

class IDModel(Model):

    @classmethod
    def parse(cls, api, json):
        if isinstance(json, list):
            return json
        else:
            return json['ids']


class JSONModel(Model):

    @classmethod
    def parse(cls, api, json):
        return json


class WelcomeMessage(Model):

    @classmethod
    def parse(cls, api, json):
        if "welcome_message" in json.keys():
            json = json["welcome_message"]
        dm = cls(api)
        setattr(dm, '_json', json)
        for k, v in json.items():
            setattr(dm, k, v)
        return dm

    @classmethod
    def parse_list(cls, api, json_list):
        if isinstance(json_list["welcome_messages"], list):
            item_list = json_list["welcome_messages"]
        else:
            item_list = [json_list["welcome_message"]]

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results
 
class Rule(Model):

    @classmethod
    def parse(cls, api, json):

        if "welcome_message_rule" in json.keys():
            json = json["welcome_message_rule"]
        dm = cls(api)
        setattr(dm, '_json', json)
        for k, v in json.items():
            setattr(dm, k, v)
        return dm

    @classmethod
    def parse_list(cls, api, json_list):
        if not json_list:
            return json_list
        if isinstance(json_list["welcome_message_rules"], list):
            item_list = json_list["welcome_message_rules"]
        else:
            item_list = json_list

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


class CustomModelFactory:
    """
    Used by parsers for creating instances
    of models. You may subclass this factory
    to add your own extended models.
    """
    welcome_message = WelcomeMessage
    rule = Rule
