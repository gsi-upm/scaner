from scaner.utils import add_metadata
import json
from flask import current_app

# thetopics = {}

# with open('examples/topics.json') as f:
#     temp = json.load(f)
#     thetopics = temp

@add_metadata('topics')
def search(*args, **kwargs):
    return {'topics': current_app.tasks.topic_search()}, 200 

@add_metadata()
def get(topicId, *args, **kwargs):
    return {'topics': current_app.tasks.topic(topicId)}, 200 

@add_metadata()
def get_network(*args, **kwargs):
    pass
