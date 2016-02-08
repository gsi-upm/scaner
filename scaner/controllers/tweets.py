import json
from scaner.utils import add_metadata

tweets = {}
with open('examples/tweets-me.json') as f:
    tweets = json.load(f)

@add_metadata
def get(tweetId, *args, **kwargs):
    for i in tweets['statuses']:
        if i['id'] == tweetId:
            return {'statuses': i}
    return {'result': "Tweet not found"}, 404
    

@add_metadata
def search(topic=None, *args, **kwargs):
    with open('examples/tweets-me.json') as f:
        example = json.load(f)
    print('Topic: %s' % topic)
    if 'statuses' in example:
        toshow = []
        for i in example['statuses']:
            if topic and topic not in i['topics']:
                print("Removing status")
                continue
            toshow.append(i)
        example['statuses'] = toshow
    example['metadata']['count'] = len(example['statuses'])
    return example

@add_metadata
def post(body, *args, **kwargs):
    print(body)
    pass

@add_metadata
def delete(*args, **kwargs):
    pass

@add_metadata
def put(*args, **kwargs):
    pass

@add_metadata
def get_history(tweetId, *args, **kwargs):
    with open('examples/history.json') as f:
        example = json.load(f)
    if example['id'] == tweetId:
        return example
    else:
        return {"id": tweetId}
