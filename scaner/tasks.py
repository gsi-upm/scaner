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
    userRecord = client.query("select userid,followers,impact,voice_t,user_relevance,UI_score,TR_score,UI_unnormalized,FR_score,voice_r from User where userid = '" + str(user_id) + "'")
    userDict = {}
    for attributeIn in userRecord[0].oRecordData:
        userDict[attributeIn] = userRecord[0].oRecordData[attributeIn]

    # En caso de que quiera sacar las relaciones
    # del userDict['in_Follows']
    # del userDict['out_Follows']
    # del userDict['in_Retweeted_by']
    # del userDict['in_Created_by']

    return json.dumps(userDict)

@celery.task
def user_network(user_id):
    userRecord = client.query("select from User where userid='{userid}'".format(userid=user_id))

@celery.task
def user_attributes(user_id, attributes):
    userRecord = client.query("select " + str(attribute) + " from User where userid = '" + str(user_id) + "'")
    userDict = {}
    for attributeIn in userRecord[0].oRecordData:
        userDict[attributeIn] = userRecord[0].oRecordData[attributeIn]
    return json.dumps(userDict)


@celery.task
def user_search(user_id, attributes_search):
    if attributes_search:
        attributes_search = attributes_search[:-2]
    userRecord = client.query("select userid, {attributes_search} from User where userid = '{userid}'".format(attributes_search=attributes_search,userid=user_id))
    userDict = {}
    for attributeIn in userRecord[0].oRecordData:
        userDict[attributeIn] = userRecord[0].oRecordData[attributeIn]
    return json.dumps(userDict)


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
    tweetRecord = client.query("select from Tweet where id = '" + str(tweet_id) + "'")
    # Procesar el tweet y eliminar los atributos de OrientDB y las metricas viejas
    return tweetRecord[0].oRecordData

@celery.task
def tweet_attributes(tweet_id, attributes):
    print (attributes)
    tweetRecord = client.query("select {attributes} from Tweet where id = '{id}'".format(attributes=attributes,id=tweet_id))
    return tweetRecord[0].oRecordData

@celery.task
def tweet_history(tweet_id):
    tweetRecord = client.query("select from Tweet where id = '" + str(tweet_id) + "'")
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