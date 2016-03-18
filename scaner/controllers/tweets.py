from flask import current_app
from scaner.utils import add_metadata
import json

# tweets = {}
# with open('examples/tweets-me.json') as f:
#     tweets = json.load(f)

@add_metadata()
def get(tweetId, fields=None, *args, **kwargs):
    if fields:
        return {'statuses': current_app.tasks.tweet_attributes(tweetId, fields)}, 200
    else:
        return {'statuses': current_app.tasks.tweet(tweetId)}, 200 

@add_metadata('statuses') #'statuses'
def search(fields='', limit=20, topic=None, sort_by=None, *args, **kwargs):
    return {'statuses': current_app.tasks.tweet_search(fields, limit, topic, sort_by)}, 200

@add_metadata()
def post(body, *args, **kwargs):
    return {'result': current_app.tasks.add_tweet(json.dumps(body))}, 200

@add_metadata()
def delete(tweetId, *args, **kwargs):
    return {'result': current_app.tasks.delete_tweet(tweetId)}, 200

@add_metadata()
def put(*args, **kwargs):
    pass

@add_metadata()
def get_history(tweetId, *args, **kwargs):
    #return {'result': current_app.tasks.tweet_history(tweetId)}, 200
    pass
