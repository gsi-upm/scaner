from scaner.utils import add_metadata
import json
from flask import current_app


@add_metadata('tasks')
def search(*args, **kwargs):	
    return {'tasks': {"celery@881243cbebfa": []}}, 200 

@add_metadata('status')
def get(taskId, *args, **kwargs):
    return {'status': "Pending"}, 200 

@add_metadata()
def get_emotions_from_twitter(*args, **kwargs):
    return {'status': 'Task running in background'}, 200 

@add_metadata()
def run_metrics(*args, **kwargs):
    return {'status': 'Task running in background'}, 200 

@add_metadata()
def update_users(*args, **kwargs):
    return {'status': 'Task running in background'}, 200 

@add_metadata()
def get_tweets_from_twitter(*args, **kwargs):
    return {'status': 'Task running in background'}, 200 