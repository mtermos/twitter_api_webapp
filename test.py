

import json


json_str ='''
{
    "welcome_message": {
        "id": "1495330066301132806",
        "created_timestamp": "1645349444352",
        "message_data": {
            "text": "Welcome!",
            "entities": {
                "hashtags": [],
                "symbols": [],
                "user_mentions": [],
                "urls": []
            }
        },
        "source_app_id": "23439693",
        "name": "simple_welcome-message 01"
    },
    "apps": {
        "23439693": {
            "id": "23439693",
            "name": "Adawat_DM",
            "url": "https://twitter-api-webapp.herokuapp.com/"
        }
    }
}
'''

json_j = json.loads(json_str)

for message in json_j['welcome_message']:
    print(message)