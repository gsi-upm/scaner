from scaner.utils import add_metadata
import json
from flask import current_app

@add_metadata('tasks')
def search(*args, **kwargs):
    return {'tasks': current_app.tasks.tasks_search()}, 200 

@add_metadata()
def get(taskId, *args, **kwargs):
    return {'tasks': current_app.tasks.task(taskId)}, 200 

@add_metadata()
def get_network(*args, **kwargs):
    pass
