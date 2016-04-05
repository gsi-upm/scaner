from flask import current_app
from scaner.utils import add_metadata
import json

# theusers = {"users": []}
# with open('examples/users.json') as f:
#     theusers = json.load(f)

# thenet = {"links": []}
# with open('examples/user_network.json') as f:
#     thenet = json.load(f)

@add_metadata()
def get(userId, fields=None, *args, **kwargs):
    if fields:
        get_task = current_app.tasks.user_attributes.delay(userId, fields)
    else:
        get_task = current_app.tasks.user.delay(userId)
    return {'users': get_task.get(timeout=10)}, 200 

@add_metadata('links')
def get_network(userId, *args, **kwargs):
    get_network_task = current_app.tasks.user_network.delay(userId)
    return {'result': get_network_task.get(timeout=10)}, 200

@add_metadata('users')
def search(fields='', limit=20, topic=None, sort_by=None, *args, **kwargs):
    search_task = current_app.tasks.user_search.delay(fields, limit, topic, sort_by)
    return {'users': search_task.get(timeout=10)}, 200

@add_metadata()
def post(body, *args, **kwargs):
    pass
    #return {'result': current_app.tasks.add_user(body)}, 200

@add_metadata()
def delete(*args, **kwargs):
    delete_task = current_app.tasks.delete_user.delay(userId)
    return {'result': delete_task.get(timeout=10)}, 200

@add_metadata()
def put(*args, **kwargs):
    pass

@add_metadata()
def get_emotion(*args, **kwargs):
    return {'result': current_app.tasks.get_user(userId)}, 200

@add_metadata()
def get_sentiment(*args, **kwargs):
    return {'result': current_app.tasks.get_user(userId)}, 200

@add_metadata()
def get_metrics(*args, **kwargs):
    return {'result': current_app.tasks.get_user(userId)}, 200
