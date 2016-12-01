from scaner.utils import add_metadata
import json
from flask import current_app

# thetopics = {}

# with open('examples/topics.json') as f:
#     temp = json.load(f)
#     thetopics = temp

@add_metadata('topics')
def search(*args, **kwargs):
    return {'topics': [{"id": 0, "name": "Topic1", "tweet_count": 364, "user_count": 146},{"id": 1, "name": "Topic2", "tweet_count": 310, "user_count": 100}]}, 200 
@add_metadata()
def get(topicId, *args, **kwargs):
    return {'topics': {"id": 0, "name": "Topic1", "tweet_count": 364, "user_count": 146}}, 200 

@add_metadata('network')
def get_network(topicId, entity, *args, **kwargs):
    if entity == "tweet":
    	return{'network': [{"id_str": "748754982564794368"},{"id_str": "748773604280508416"},{"id_str": "751749464617091072"},{"id_str": "752819665374703616"}]}, 200
    if entity == "user":
    	return{'network': [{"id_str": "2359753596"},{"id_str": "1954830398"},{"id_str": "104832840"},{"id_str": "2900486920"}]}, 200
    else:
    	return {'network': "Wrong entity"}

