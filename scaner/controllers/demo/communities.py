from flask import current_app
from scaner.utils import add_metadata
import json

# PRUEBA EXTRACION USUARIOS
# @add_metadata()
# def get(userId, fields=None, *args, **kwargs):
#     #get_task = current_app.tasks.get_users_from_twitter.delay()
#     get_task = current_app.tasks.execute_metrics.delay()
#     return {'result': "In progress"}, 200 

@add_metadata()
def get(communityId, *args, **kwargs):
    return {'communities': {"id":0,"user_count":23, "sentiment": "positive", "emotion": "joy"}}, 200

@add_metadata('users')
def get_network(communityId, *args, **kwargs):
    return {'users': [{"id": 783944537613951000},{"id": 783904269422497800},{"id": 782765709810163700},{"id": 314009793},{"id": 768700851598884900},{"id": 304940474}]}, 200

@add_metadata('communities')
def search(*args, **kwargs):
    return {'communities': [{"id": 0,"user_count": 12, "sentiment": "positive", "emotion": "joy"},{"id": 1,"user_count": 32, "sentiment": "positive", "emotion": "joy"},{"id": 2,"user_count": 8, "sentiment": "positive", "emotion": "joy"}]}, 200

@add_metadata()
def get_emotion(communityId, *args, **kwargs):
    return {'result': {"id": 0, "emotion": "negative-fear"}}, 200

@add_metadata()
def get_sentiment(communityId, *args, **kwargs):
    return {'result': {"id": 0, "sentiment": "positive"}}, 200