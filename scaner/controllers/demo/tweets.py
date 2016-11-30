from flask import current_app
from scaner.utils import add_metadata
import json
# from time import sleep


@add_metadata()
def get(tweetId, fields=None, *args, **kwargs):
    return {'statuses':[{"id_str": "748754982564794368", "text": "RT @gzugazua: LABORAL KUTXA. Apoy a #Baskonia en los aos duros...y juntos fuimos a Berlin. Milesker https://t.co/7NKkspxDJV", "topics": ["LaboralKutxa"]}]}, 200

@add_metadata('statuses') #'statuses'
def search(fields='', limit=20, topic=None, sort_by=None, *args, **kwargs):
    return {'statuses':[{"id_str": "748754982564794368", "text": "RT @gzugazua: LABORAL KUTXA. Apoy a #Baskonia en los aos duros...y juntos fuimos a Berlin. Milesker https://t.co/7NKkspxDJV", "topics": ["LaboralKutxa"]}]}, 200

@add_metadata()
def post(body, *args, **kwargs):
    return {'result': 'Tweet added to DB'}, 200

@add_metadata()
def delete(tweetId, *args, **kwargs):
    return {'result': 'Tweet deleted from DB'}, 200

@add_metadata()
def put(*args, **kwargs):
    pass

@add_metadata()
def get_history(tweetId, *args, **kwargs):
    return {'result': [{"complete": True, "date": "2016-11-03", "id": 748754982564794400, "influence": 0, "lastMetrics": True, "relevance": 0, "timestamp": 1478173197.8483965, "topic": "LaboralKutxa" },{"complete": True, "date": "2016-11-03", "id": 748754982564794400, "influence": 0, "lastMetrics": False, "relevance": 0, "timestamp": 1478172146.6711538,  "topic": "LaboralKutxa" }]}, 200

@add_metadata()
def get_emotion(tweetId, *args, **kwargs):
    return {'result': {"id": 0, "emotion": "negative-fear"}}, 200

@add_metadata()
def get_sentiment(tweetId, *args, **kwargs):
    return {'result': {"id": 0, "sentiment": "negative"}}, 200

@add_metadata()
def get_metrics(tweetId, *args, **kwargs):
    return {'result': {"complete": True, "date": "2016-10-03", "id": 748754982564794400, "influence": 0, "lastMetrics": True, "relevance": 0, "timestamp": 1478173197.8483965, "topic": "LaboralKutxa" }}, 200
