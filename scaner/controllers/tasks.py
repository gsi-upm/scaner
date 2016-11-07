from scaner.utils import add_metadata
import json
from flask import current_app


@add_metadata('tasks')
def search(*args, **kwargs):	
    return {'tasks': current_app.tasks.get_task_list()}, 200 

@add_metadata('status')
def get(taskId, *args, **kwargs):
    return {'status': current_app.tasks.get_task_status(taskId)}, 200 

@add_metadata()
def get_emotions_from_twitter(*args, **kwargs):
    return {'status': current_app.tasks.get_emotions_from_tweets()}, 200 

@add_metadata()
def run_metrics(*args, **kwargs):
    metricstask = current_app.tasks.execute_metrics.delay()
    return {'status': "Background"}, 200 

@add_metadata()
def update_users(*args, **kwargs):
    return {'status': current_app.tasks.get_users_from_twitter()}, 200 

@add_metadata()
def get_tweets_from_twitter(*args, **kwargs):
    return {'status': current_app.tasks.get_tweets_by_id()}, 200 