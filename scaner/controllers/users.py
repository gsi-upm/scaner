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
def get(userId, fields=None, *args, **kwargs):
    if fields:
        get_task = current_app.tasks.user_attributes.delay(userId, fields)
    else:
        get_task = current_app.tasks.user.delay(userId)
    return {'users': get_task.get(timeout=10)}, 200 

@add_metadata()
def get_network(userId, *args, **kwargs):
    get_network_task = current_app.tasks.user_network.delay(userId)
    return {'result': get_network_task.get(timeout=10)}, 200

@add_metadata('users')
def search(fields='', limit=20, topic=None, sort_by=None, *args, **kwargs):
    search_task = current_app.tasks.user_search.delay(fields, limit, topic, sort_by)
    return {'users': search_task.get(timeout=10)}, 200

@add_metadata()
def post(body, *args, **kwargs):
    post_task = current_app.tasks.add_user.delay(json.dumps(body))
    return {'result': post_task.get(interval=0.1)}, 200
 

@add_metadata()
def delete(userId, *args, **kwargs):
    delete_task = current_app.tasks.delete_user.delay(userId)
    return {'result': delete_task.get(timeout=10)}, 200

@add_metadata()
def put(*args, **kwargs):
    pass

@add_metadata()
def get_emotion(userId, *args, **kwargs):
    emotion_task = current_app.tasks.get_user_emotion.delay(userId)
    return {'result': emotion_task.get(timeout=10)}, 200

@add_metadata()
def get_sentiment(userId, *args, **kwargs):
    sentiment_task = current_app.tasks.get_user_sentiment.delay(userId)
    return {'result': sentiment_task.get(timeout=10)}, 200

@add_metadata()
def get_metrics(userId, *args, **kwargs):
    get_metrics_task = current_app.tasks.get_user_metrics.delay(userId)
    return {'result': get_metrics_task.get(timeout=10)}, 200

@add_metadata()
def followers_rel(*args, **kwargs):
    followers_rel_task = current_app.tasks.followers_rel.delay()
    return {'result': 'Background task'}, 200
 