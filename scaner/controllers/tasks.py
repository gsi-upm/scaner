from scaner.utils import add_metadata
import json
from flask import current_app


@add_metadata('tasks')
def search(*args, **kwargs):	
    return {'tasks': current_app.tasks.get_task_list()}, 200 

@add_metadata('status')
def get(taskId, *args, **kwargs):
    return {'status': current_app.tasks.get_task_status(taskId)}, 200 
