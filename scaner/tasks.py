from celery import Celery
from celery.decorators import periodic_task
import pyorient
import json
import os
import bitter.crawlers
import bitter.utils
from datetime import timedelta
from . import influence_metrics
import time
from celery.task.control import inspect
from celery.result import AsyncResult

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

REDIS_HOST = os.environ.get('REDIS_HOST')
ORIENTDB_HOST = os.environ.get('ORIENTDB_HOST')


# CONFIGURACION PARA DOCKER
# config = {}
# config['SECRET_KEY'] = 'password'
# config['CELERY_BROKER_URL'] = 'redis://%s:6379/0' % REDIS_HOST
# config['CELERY_RESULT_BACKEND'] = 'redis://%s:6379/0' % REDIS_HOST
# celery = Celery("prueba", broker='redis://%s:6379/0' % REDIS_HOST)
# celery.conf.update(config)

# client = pyorient.OrientDB(ORIENTDB_HOST, 2424)
# session_id = client.connect("root", "root")
# client.db_open("mixedemotions", "admin", "admin")

# # CONFIGURACION PARA LOCAL
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
    user = userRecord[0].oRecordData
    user.pop("in_Created_by", None)
    user.pop("in_Follows", None)
    user.pop("out_Follows", None)
    user.pop("in_Retweeted_by", None)
    user.pop("pending", None)
    return user

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
    for user_record in user_search:
        user = user_record.oRecordData
        user.pop("in_Created_by", None)
        user.pop("in_Follows", None)
        user.pop("out_Follows", None)
        user.pop("in_Retweeted_by", None)
        user.pop("pending", None)
        user_list.append(user)
    return user_list

@celery.task
def get_user_emotion(user_id):
    emotionRecord = client.query("select expand(out('hasEmotionSet')) from User where id = '{user_id}'".format(user_id=user_id))   
    return emotionRecord[0].oRecordData

@celery.task
def get_user_sentiment(user_id):
    emotionRecord = client.query("select expand(out('hasEmotionSet')) from User where id = '{user_id}'".format(user_id=user_id))   
    return emotionRecord[0].oRecordData

@celery.task
def get_user_metrics(user_id):
    metricsRecord = client.query("select expand(out('Last_metrics')) from User where id = '{user_id}'".format(user_id=user_id))   
    return metricsRecord[0].oRecordData

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
    tweetRecord = client.query("select from Tweet where id = {tweet_id}".format(tweet_id=tweet_id))
    # Procesar el tweet y eliminar los atributos de OrientDB y las metricas viejas
    tweet = tweetRecord[0].oRecordData
    tweet.pop("out_Created_by", None)
    tweet.pop("in_Retweet", None)
    tweet.pop("out_Retweet", None)
    tweet.pop("out_Retweeted_by", None)
    tweet.pop("out_Belongs_to_topic", None)
    return tweet

@celery.task
def tweet_attributes(tweet_id, attributes):
    tweetRecord = client.query("select {attributes} from Tweet where id = {id}".format(attributes=attributes,id=tweet_id))
    return tweetRecord[0].oRecordData

@celery.task
def tweet_history(tweet_id):
    tweet = tweetRecord[0].oRecordData
    tweet.pop("out_Created_by", None)
    tweet.pop("in_Retweet", None)
    tweet.pop("out_Retweet", None)
    tweet.pop("out_Retweeted_by", None)
    tweet.pop("out_Belongs_to_topic", None)
    return tweet

@celery.task
def add_tweet(tweetJson):
   # tweetJson = tweetJson.decode('utf-8', errors='ignore')
    tweetDict = json.loads(tweetJson)
    print (tweetDict['id'])
    tweetJson = json.dumps(tweetDict, ensure_ascii=False).encode().decode('ascii', errors='ignore')
    cmd = "insert into Tweet content {tweetJson}".format(tweetJson=tweetJson)
    # cmd = cmd.encode('utf-8', 'ignore')
    # logger.error(cmd)
    client.command(cmd)
    # Si es un retweet, lo enlazamos con su original
    # user_id = tweetJson['user_id']
    # print("USER ID")
    # print(user_id)
    # user = client.query("select from User where id = {id}".format(id=user_id))
    # if not user:
    #     client.command("insert into User set id = {id}, pending=True".format(id=user_id))
    # client.command("create edge Created_by from (select from Tweet where id = {tweet_id}) to (select from User where id = {user_id})".format(tweet_id=tweetJson['id'],user_id=user_id))
    # if tweetJson['retweeted_status']:
    #     client.command("create edge Retweet from (select from Tweet where id = {retweet}) to (select from Tweet where id = {original})".format(retweet=tweetJson['id'], original=tweetJson['retweeted_status']['id']))
    #     client.command("create edge Retweeted_by from (Tweet where id = {original}) to (select from User where id = {user_id})".format(original=tweetJson['retweeted_status']['id'], user_id=user_id))
    return ("Tweet added to DB")

@celery.task
def delete_tweet(tweet_id):
    client.command("delete vertex from Tweet where id = {id}".format(id=tweet_id))
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
    for tweet_record in tweet_search:
        tweet = tweet_record.oRecordData
        tweet.pop("out_Created_by", None)
        tweet.pop("in_Retweet", None)
        tweet.pop("out_Retweet", None)
        tweet.pop("out_Retweeted_by", None)
        tweet.pop("out_Belongs_to_topic", None)
        tweet_list.append(tweet)
    return tweet_list

@celery.task
def get_tweet_emotion(tweet_id):
    emotionRecord = client.query("select expand(out('hasEmotionSet')) from Tweet where id = '{tweet_id}'".format(tweet_id=tweet_id))   
    return emotionRecord[0].oRecordData

@celery.task
def get_tweet_sentiment(tweet_id):
    emotionRecord = client.query("select expand(out('hasEmotionSet')) from Tweet where id = '{tweet_id}'".format(tweet_id=tweet_id))   
    return emotionRecord[0].oRecordData

@celery.task
def get_tweet_metrics(tweet_id):
    metricsRecord = client.query("select expand(out('Last_metrics')) from Tweet where id = '{tweet_id}'".format(tweet_id=tweet_id))   
    return metricsRecord[0].oRecordData

@celery.task
def topic_search():
    topicList = client.query("select from Topic")
    topic_list = []
    for topic in topicList:
        topic = topic.oRecordData
        topic.pop("in_Belongs_to_topic", None)
        topic_list.append(topic)
    return topic_list

@celery.task
def topic(topic_id):
    topicRecord = client.query("select from Topic where id = {topic_id}".format(topic_id=topic_id))
    # Procesar el topic y eliminar los atributos de OrientDB
    topic = topicRecord[0].oRecordData
    topic.pop("in_Belongs_to_topic", None)
    return topic

@celery.task
def topic_network(topic_id):
    pass

#@periodic_task(run_every=timedelta(days=1))
#@periodic_task(run_every=timedelta(seconds=30))
@celery.task
def get_users_from_twitter(pending_users=None):
    print("TAREA PERIODICA")
    wq = bitter.crawlers.TwitterQueue.from_credentials('credentials.json')
    if not pending_users:
        pending_users = client.query("select id from User limit -1")
    pending_user_list = []
    for user in pending_users:
        pending_user_list.append(user)
    for user in bitter.utils.get_users(wq,pending_user_list):
        client.command("delete vertex User where id = {id}".format(id=user.id))
        client.command("insert into User content {user}".format(user=user))
        client.command("update User set pending = false where id = {id}".format(id=user.id))

        client.command("create edge Created_by from (select from Tweet where user_id = {id} to (select from User where id = {id})".format(id=user.id))
        client.command("create edge Retweeted_by from (select expand(out('Retweet')) from (select from Tweet where user_id = {id})) to (select from User where id={id})".format(id=user.id))

        #TODO RELACION FOLLOW

@celery.task
def get_task_list():
    i = inspect()
    return i.scheduled()
    
@celery.task
def get_task_status(taskId):
    res = AsyncResult(taskId)
    return str(res.ready())

# @periodic_task(run_every=timedelta(days=1))
# def execute_metrics():
#     influence_metrics.execution()

@celery.task
def get_user_of_tweet(tweetId):
    wq = bitter.crawlers.TwitterQueue.from_credentials('credentials.json')
    # pending_user = client.query("select user.id from Tweet where id = {tweetId}".format(tweetId=tweetId))
    # logger.error(pending_user[0].oRecordData)
    # pending_user_list = [pending_user[0].oRecordData['id']]
    pending_user_list = ["88602264",]
    users_retrieved = bitter.utils.get_users(wq,pending_user_list)
    for user_extracted in users_retrieved:
        user_final = json.dumps(user_extracted, ensure_ascii=False).encode().decode('ascii', errors='ignore')
        logger.error(user_final)
        client.command("insert into User content {user}".format(user=user_final))
    return "success"