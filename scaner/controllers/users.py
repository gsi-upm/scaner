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
        return {'users': current_app.tasks.user_attributes(userId, fields)}, 200
    else:
        return {'users': current_app.tasks.user(userId)}, 200 

@add_metadata('links')
def get_network(userId, *args, **kwargs):
    return {'result': current_app.tasks.user_network(userId)}, 200

@add_metadata('users')
def search(fields='', limit=20, topic=None, sort_by=None, *args, **kwargs):
    return {'users': current_app.tasks.user_search(fields, limit, topic, sort_by)}, 200

@add_metadata()
def post(body, *args, **kwargs):
    pass
    #return {'result': current_app.tasks.add_user(body)}, 200

@add_metadata()
def delete(*args, **kwargs):
    return {'result': current_app.tasks.delete_user(userId)}, 200

@add_metadata()
def put(*args, **kwargs):
    pass

@add_metadata()
def get_emotion(*args, **kwargs):
    return {'result': current_app.tasks.delete_user(userId)}, 200
