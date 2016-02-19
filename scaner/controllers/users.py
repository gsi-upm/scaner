from scaner.utils import add_metadata
import json

# theusers = {"users": []}
# with open('examples/users.json') as f:
#     theusers = json.load(f)


# thenet = {"links": []}
# with open('examples/user_network.json') as f:
#     thenet = json.load(f)

@add_metadata()
def get(userId, *args, **kwargs):
    # for i in theusers['users']:
    #     if i['id'] == userId:
    #         return i
    return tasks.user()

@add_metadata('links')
def get_network(userId, *args, **kwargs):
    # result = thenet.copy()
    # result['links'] = []
    # print(thenet)
    # for i in thenet['links']:
    #     print(i.values())
    #     if userId in list(i.values()):
    #         result['links'].append(i)
    # return result
    return tasks.user_network()

@add_metadata('users')
def search(topic=None, *args, **kwargs):
    # result = theusers.copy()
    # result['users'] = []
    # for i in theusers['users']:
    #     if not topic or topic in i['topics']:
    #         result['users'].append(i)
    # return result
    return tasks.user_search()

@add_metadata()
def post(*args, **kwargs):
    pass

@add_metadata()
def delete(*args, **kwargs):
    pass

@add_metadata()
def put(*args, **kwargs):
    pass
