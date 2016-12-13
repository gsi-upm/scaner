from flask import current_app
from scaner.utils import add_metadata
import json

# PRUEBA EXTRACION USUARIOS
# @add_metadata()
# def get(userId, fields=None, *args, **kwargs):
#     #get_task = current_app.tasks.get_users_from_twitter.delay()
#     get_task = current_app.tasks.execute_metrics.delay()
#     return {'result': "In progress"}, 200 

@add_metadata('communities')
def get(communityId, *args, **kwargs):
    get_task = current_app.tasks.get_community.delay(communityId)
    return {'communities': get_task.get(timeout = 100)}, 200

@add_metadata('users')
def get_network(communityId, *args, **kwargs):
    community_network_task = current_app.tasks.get_community_network.delay(communityId)
    return {'users': community_network_task.get(timeout = 100)}, 200

@add_metadata('communities')
def search(*args, **kwargs):
    search_task = current_app.tasks.get_communities_list.delay()
    return {'communities': search_task.get(timeout = 100)}, 200

@add_metadata()
def get_emotion(communityId, *args, **kwargs):
    return {'result': {"id": 0, "emotion": "negative-fear"}}, 200

@add_metadata()
def get_sentiment(communityId, *args, **kwargs):
    sentiment_task = current_app.tasks.get_community_sentiment.delay(communityId)
    return {'communities': sentiment_task.get(timeout = 100)}, 200