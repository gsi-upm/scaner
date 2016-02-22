from celery import Celery
import pyorient
import json

config = {}
config['SECRET_KEY'] = 'password'
config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery("prueba", broker='redis://localhost:6379/0')
celery.conf.update(config)

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "root")
client.db_open("mixedemotions", "admin", "admin")


@celery.task
def user(user_id):
    userRecord = client.query("select from User where id = '{user_id}'".format(user_id=user_id))
    return userRecord[0].oRecordData

#TODO
@celery.task
def user_network(user_id):
    userRecord = client.query("select from User where id='{userid}'".format(userid=user_id))

@celery.task
def user_attributes(user_id, attributes):
    userRecord = client.query("select {attributes} from User where id = '{user_id}'".format(attributes=attributes, user_id=user_id))
    return userRecord[0].oRecordData


@celery.task
def user_search(attributes, limit, topic, sort_by):
    if topic:
        if sort_by:
            user_search = client.query("select {attributes} from User where topics containsValue {topic} order by {sort_by} limit {limit}".format(attributes=attributes, topic=topic, sort_by=sort_by, limit=limit))
        else:
            user_search = client.query("select {attributes} from User where topics containsValue {topic} limit {limit}".format(attributes=attributes, topic=topic, limit=limit))
    elif sort_by:
        user_search = client.query("select {attributes} from User order by {sort_by} limit {limit}".format(attributes=attributes, sort_by=sort_by, limit=limit))
    else:
        user_search = client.query("select {attributes} from User limit {limit}".format(attributes=attributes, limit=limit))
    # Procesar los usuarios y eliminar los atributos de OrientDB y las metricas viejas
    user_list=[]
    for user in user_search:
        user_list.append(user.oRecordData)
    return user_list

@celery.task
def prueba():
    return "prueba"

@celery.task
def ranking_users():
    rankingRecord = client.query("select from User order by user_relevance desc limit 20")
    ranking=[]
    for n, user in enumerate(rankingRecord):
        ranking.append("En el puesto numero " + str(n+1) + " tenemos al usuario " + str(user.oRecordData['userid']))
    return json.dumps(ranking)

@celery.task
def ranking_tweets():
    rankingRecord = client.query("select from Tweet order by tweet_relevance desc limit 20")
    ranking=[]
    for n, tweet in enumerate(rankingRecord):
        ranking.append("En el puesto numero " + str(n+1) + " tenemos el tweet " + str(tweet.oRecordData['tid']))
    return json.dumps(ranking)

@celery.task
def tweet(tweet_id):
    tweetRecord = client.query("select from Tweet where id = '{tweet_id}'".format(tweet_id=tweet_id))
    # Procesar el tweet y eliminar los atributos de OrientDB y las metricas viejas
    return tweetRecord[0].oRecordData

@celery.task
def tweet_attributes(tweet_id, attributes):
    print (attributes)
    tweetRecord = client.query("select {attributes} from Tweet where id = '{id}'".format(attributes=attributes,id=tweet_id))
    return tweetRecord[0].oRecordData

@celery.task
def tweet_history(tweet_id):
    tweetRecord = client.query("select from Tweet where id = '{tweet_id}'".format(tweet_id=tweet_id))
    return tweetRecord[0].oRecordData

@celery.task
def add_tweet(tweetJson):
    client.command("insert into Tweet content {tweetJson}".format(tweetJson=tweetJson))
    return ("Tweet added to DB")

@celery.task
def delete_tweet(tweet_id):
    client.command("delete vertex from Tweet where id='{id}'".format(id=tweet_id))
    return ("Tweet deleted from DB")

@celery.task
def tweet_search(attributes, limit, topic, sort_by):
    # Revisar la forma de hacer la búsqueda
    if topic:
        if sort_by:
            tweet_search = client.query("select {attributes} from Tweet where topics containsValue {topic} order by {sort_by} limit {limit}".format(attributes=attributes, topic=topic, sort_by=sort_by, limit=limit))
        else:
            tweet_search = client.query("select {attributes} from Tweet where topics containsValue {topic} limit {limit}".format(attributes=attributes, topic=topic, limit=limit))
    elif sort_by:
        tweet_search = client.query("select {attributes} from Tweet order by {sort_by} limit {limit}".format(attributes=attributes, sort_by=sort_by, limit=limit))
    else:
        tweet_search = client.query("select {attributes} from Tweet limit {limit}".format(attributes=attributes, limit=limit))
    # Procesar los tweets y eliminar los atributos de OrientDB y las metricas viejas
    tweet_list=[]
    for tweet in tweet_search:
        tweet_list.append(tweet.oRecordData)
    return tweet_list