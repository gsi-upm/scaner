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
    return {'users': {"id": 2359753596, "location": "", "topics": ["LaboralKutxa"]}}, 200 

@add_metadata('users')
def get_network(userId, *args, **kwargs):
    return {'users': [{"id": 2819306356},{"id": 2288478043},{"id": 452459062}]}, 200

@add_metadata('users')
def search(fields='', limit=20, topic=None, sort_by=None, *args, **kwargs):
    return {'users': [{"id": 2359753596, "location": "", "topics": ["LaboralKutxa"]},{"id": 1954830398, "location": "", "topics": ["LaboralKutxa"]},{"id": 104832840,"location": "","topics": ["LaboralKutxa"]},{"id": 2900486920,"location": "Belgrade, Republic of Serbia","topics": ["LaboralKutxa"]}]}, 200

@add_metadata()
def post(body, *args, **kwargs):
    pass
    #return {'result': current_app.tasks.add_user(body)}, 200

@add_metadata()
def delete(userId, *args, **kwargs):
    return {'result': 'User deleted from DB'}, 200

@add_metadata()
def put(*args, **kwargs):
    pass

@add_metadata()
def get_emotion(*args, **kwargs):
    return {'result': {"id": 0, "emotion": "negative-fear"}}, 200

@add_metadata()
def get_sentiment(*args, **kwargs):
    return {'result': {"id": 0, "sentiment": "positive"}}, 200

@add_metadata()
def get_metrics(userId, *args, **kwargs):
    return {'result': {"complete": False, "date": "2016-07-14", "followers": 47590, "following": 352, "id": 84333477, "impact": 0.34644, "influence": 0.87433, "influenceUnnormalized": 0, "lastMetrics": True, "relevance": 0.94873894, "statuses_count": 50621, "tweetRatio": 0.47471, "voice": 0.23482734, "voice_r": 0}}, 200

def get_ranking(ranking, *args, **kwargs):
    if ranking == 'voice':
        return {'ranking': [{"id": 2819306356, "voice":0.847783},{"id": 2288478043, "voice":0.647783},{"id": 452459062, "voice":0.347783}]}, 200
    if ranking == 'impact':
        return {'ranking': [{"id": 2819306356, "impact":0.847783},{"id": 2288478043, "impact":0.847783},{"id": 452459062, "impact":0.847783}]}, 200
    if ranking == 'influence':
        return {'ranking': [{"id": 2819306356, "influence":0.847783},{"id": 2288478043, "influence":0.847783},{"id": 452459062, "influence":0.847783}]}, 200
    if ranking == 'relevance':
        return {'ranking': [{"id": 2819306356, "relevance":0.847783},{"id": 2288478043, "relevance":0.847783},{"id": 452459062, "relevance":0.847783}]}, 200
    else:
        return "Wrong parameter"