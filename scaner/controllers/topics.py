from scaner.utils import add_metadata
import json

thetopics = {}

with open('examples/topics.json') as f:
    temp = json.load(f)
    thetopics = temp

@add_metadata('topics')
def search(*args, **kwargs):
     return thetopics

@add_metadata()
def get(topicId, *args, **kwargs):
    for i in thetopics['topics']:
        if topicId == i['id']:
            return i
    return {}

@add_metadata()
def get_network(*args, **kwargs):
    pass
