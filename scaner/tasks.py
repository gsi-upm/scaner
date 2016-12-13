from celery import Celery
from celery.decorators import periodic_task
from celery.schedules import crontab
import pyorient
import json
import os
import bitter.crawlers
import bitter.utils
import math
import time
from itertools import islice
import requests
from datetime import timedelta
import datetime
from time import sleep, mktime
from . import influence_metrics
from . import compute_communities
#from time import sleep
from celery.task.control import inspect
from celery.task.control import revoke
from celery.result import AsyncResult
from twitter import TwitterHTTPError
from celery.utils.log import get_task_logger
from billiard.exceptions import Terminated

logger = get_task_logger(__name__)

REDIS_HOST = os.environ.get('REDIS_HOST')
ORIENTDB_HOST = os.environ.get('ORIENTDB_HOST')

# CONFIGURACION PARA DOCKER
config = {}
config['SECRET_KEY'] = 'password'
config['CELERY_BROKER_URL'] = 'redis://%s:6379/0' % REDIS_HOST
config['CELERY_RESULT_BACKEND'] = 'redis://%s:6379/0' % REDIS_HOST
celery = Celery("prueba", broker='redis://%s:6379/0' % REDIS_HOST)
celery.conf.update(config)

client = pyorient.OrientDB(ORIENTDB_HOST, 2424)
session_id = client.connect("root", "root")
client.db_open("mixedemotions", "admin", "admin")

# CONFIGURACION PARA LOCAL
# config = {}
# config['SECRET_KEY'] = 'password'
# config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# #config['ONCE_DEFAULT_TIMEOUT'] = 18000
# celery = Celery("prueba", broker='redis://localhost:6379/0')
# celery.conf.update(config)

# client = pyorient.OrientDB("localhost", 2424)
# session_id = client.connect("root", "root")
# client.db_open("mixedemotions", "admin", "admin")

#LISTA DE ATRIBUTOS A ELIMINAR DE LAS PETICIONES A ORIENTDB
delete_variables = ("in_Created_by","in_Follows","out_Follows","in_Retweeted_by","pending","out_Last_metrics","out_Created_by","in_Retweet","out_Retweet","out_Retweeted_by","out_Belongs_to_topic","out_Replied_by","in_Reply","out_Reply","out_Belongs_to_Community","in_Belongs_to_Community")

@celery.task
def user(user_id):
    try:
        userRecord = client.query("select from User where id_str = '{user_id}'".format(user_id=user_id))
        user = userRecord[0].oRecordData
        for k in delete_variables:
            if user.get(k):
                del user[k]
        return user
    except:
        return "User not found in DB"

#TODO
@celery.task
def user_network(user_id):
    user_followers = client.query("select id from (select expand(in('Follows')) from User where id='{userid}' limit -1) limit -1".format(userid=user_id))
    user_follower_list=[]
    for user_record in user_followers:
        user = user_record.oRecordData
        #print(user)
        user_follower_list.append(user)
    return user_follower_list

@celery.task
def user_attributes(user_id, attributes):
    userRecord = client.query("select {attributes} from User where id = '{user_id}'".format(attributes=attributes, user_id=user_id))
    return userRecord[0].oRecordData

@celery.task
def user_search(attributes, limit, topic, sort_by):
    if topic:
        if sort_by:
            user_search = client.query("select {attributes} from User where topics containsText '{topic}' order by {sort_by} limit {limit}".format(attributes=attributes, topic=topic, sort_by=sort_by, limit=limit))
        else:
            user_search = client.query("select {attributes} from User where topics containsText '{topic}' limit {limit}".format(attributes=attributes, topic=topic, limit=limit))
    elif sort_by:
        user_search = client.query("select {attributes} from User order by {sort_by} limit {limit}".format(attributes=attributes, sort_by=sort_by, limit=limit))
    else:
        user_search = client.query("select {attributes} from User limit {limit}".format(attributes=attributes, limit=limit))
    # Procesar los usuarios y eliminar los atributos de OrientDB y las metricas viejas
    user_list=[]
    for user_record in user_search:
        user = user_record.oRecordData
        for k in delete_variables:
            if user.get(k):
                del user[k]
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
    try:
        metricsRecord = client.query("select expand(out('Last_metrics')) from User where id = '{user_id}'".format(user_id=user_id))   
        user_metrics = metricsRecord[0].oRecordData
        user_metrics.pop("in_Last_metrics")
        return user_metrics
    except:
        return "User metrics have not been calculated yet"

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
    try:
        tweetRecord = client.query("select from Tweet where id_str = {tweet_id}".format(tweet_id=tweet_id))
        # Procesar el tweet y eliminar los atributos de OrientDB y las metricas viejas
        tweet = tweetRecord[0].oRecordData
        for k in delete_variables:
            if tweet.get(k):
                del tweet[k]
        return tweet
    except:
        return "Tweet not found in DB"

@celery.task
def tweet_attributes(tweet_id, attributes):
    try:
        tweetRecord = client.query("select {attributes} from Tweet where id_str = {id}".format(attributes=attributes,id=tweet_id))
        return tweetRecord[0].oRecordData
    except:
        return "Tweet not found in DB"

@celery.task
def tweet_history(tweet_id):
    tweet_history = client.query("select from (select from Tweet_metrics where id = {tweet_id} limit 10) order by timestamp desc".format(tweet_id=tweet_id))
    tweet_history_list=[]

    for tweet_record in tweet_history:
        tweet = tweet_record.oRecordData
        tweet.pop("in_Last_metrics", None)
        #print(tweet)
        tweet_history_list.append(tweet_record.oRecordData)
    return tweet_history_list
@celery.task
def add_user(userJson, topics=None):
    print("User recibido")
    
    userDict = json.loads(userJson)
    if topics:
        userDict['topics'] = topics
    for topic in userDict['topics']:
        topicInDB = client.query("select from Topic where name = '{topic}'".format(topic=topic))
        if not topicInDB:
            num_topics = client.query("select count(*) from Topic")[0].oRecordData['count']
            cmd = "insert into Topic set name = '{topic}', id = {id}, tweet_count = 0, user_count = 0".format(topic=topic, id=num_topics)
            logger.warning(cmd)
            client.command(cmd)

    logger.info(userDict)
    userInDB = client.query("select id from User where id = {id}".format(id=userDict['id']))
    if not userInDB:
        userJson = json.dumps(userDict, ensure_ascii=False).encode().decode('ascii', errors='ignore')
        client.command("insert into User content {content}".format(content=userJson))
        client.command('update User set pending=True, depth=0 where id={id}'.format(id=userDict['id']))
        for topic in userDict['topics']:
            cmd = "create edge Belongs_to_topic from (select from User where id = {user_id}) to (select from Topic where name = '{topic}')".format(user_id=userDict['id'], topic=topic)
            client.command(cmd)
            ts = time.time()
            date_ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            client.command("insert into User_metrics set id = {id}, lastMetrics = True, topic = '{topic}', followers = {followers}, following = {following}, date = '{date}', statuses_count = {statuses_count}, timestamp = {timestamp}, tweetRatio = 0, influence = 0, influenceUnnormalized = 0, voice = 0, voice_r = 0, impact = 0, relevance = 0, complete = False".format(id=userDict['id'],followers=userDict['followers_count'],following=userDict['friends_count'], topic= topic, date = date_ts, timestamp = ts, statuses_count = userDict['statuses_count']))    
    else:
        print("User exists in DB")
        if 'friends_ids' in userDict:
            client.command("update User set friends_ids = {friends_ids}, screen_name = '{screen_name}',followers_count= {followers_count}, protected = {protected}, friends_count = {friends_count}, lang = {lang}, statuses_count = {statuses_count}, pending=True where id={id}".format(friends_ids=userDict['friends_ids'],id=userDict['id'],screen_name=userDict['screen_name'], statuses_count = userDict['statuses_count'], followers_count = userDict['followers_count'], friends_count = userDict['friends_count'], protected = userDict['protected'], lang = userDict['lang'], created_at = userDict['created_at']))
        ts = time.time()
        date_ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        for topic in userDict['topics']:
            client.command("insert into User_metrics set id = {id}, lastMetrics = True, topic = '{topic}', followers = {followers}, following = {following}, date = '{date}', statuses_count = {statuses_count}, timestamp = {timestamp}, tweetRatio = 0, influence = 0, influenceUnnormalized = 0, voice = 0, voice_r = 0, impact = 0, relevance = 0, complete = False".format(id=userDict['id'],followers=userDict['followers_count'],following=userDict['friends_count'], topic= topic, date = date_ts, timestamp = ts, statuses_count = userDict['statuses_count']))    



# SOLO DATASET DE NORO 
@celery.task
def followers_rel():
    #pending_users = client.query("select id, screen_name from User skip {skip} limit {limit}".format(skip=skip, limit=limit))
    pending_users = client.query("select id,friends_ids from User where pending = true limit -1")
    pending_user_list = []
    for user in pending_users:
        pending_user_list.append({'id':user.oRecordData['id'],'friends_ids':user.oRecordData['friends_ids']})

    for user_friends in pending_user_list:
        if user_friends['friends_ids'] == []:
            client.command('update User set pending=False where id={id}'.format(id=user_friends['id']))
        else:    
            for friend in user_friends['friends_ids']:
                friend_id = client.query("select id from User where screen_name='{friend}'".format(friend=str(friend)))
                if friend_id:
                    friend_id = friend_id[0].oRecordData['id']
                    cmd = "create edge Follows from (select from User where id = {user_id}) to (select from User where id = {following_id})".format(user_id=user_friends['id'], following_id=friend_id)
                    client.command(cmd)
            client.command('update User set pending=False, depth = 0 where id={id}'.format(id=user_friends['id']))
    print(':FIN:')

#Metodo alternativo para cargar tweets
@celery.task
def add_tweet_raw(tweetJson):
    tweetDict = json.loads(tweetJson)
    tweetDict['pending'] = True
    tweetInDB = client.query("select id_str from Tweet where id_str = '{id}'".format(id=tweetDict['id_str']))
    tweet_topics = tweetDict['topics']
    if tweetInDB:
        return ("Tweet already in DB")
    else:
        tweetJson = json.dumps(tweetDict, ensure_ascii=False).encode().decode('ascii', errors='ignore')
        cmd = "insert into Tweet content {tweetJson}".format(tweetJson=tweetJson)
        client.command(cmd)

    for topic in tweet_topics:
        cmd = "create Edge Belongs_to_topic from (select from Tweet where id_str = '{tweet_id}') to (select from Topic where name = '{topic}')".format(tweet_id=tweetDict['id_str'], topic=topic)
        client.command(cmd)

    try:    
        cmd = ("create edge Created_by from (select from Tweet where id_str = '{tweet_id}') to (select from User where id = {user_id})".format(tweet_id=tweetDict['id_str'],user_id=tweetDict['user']['id']))
        print(cmd)
        client.command(cmd)
    except:
        print("User not in DB")
        add_user(json.dumps(tweetDict['user']),tweet_topics)    
        cmd = ("create edge Created_by from (select from Tweet where id_str = '{tweet_id}') to (select from User where id = {user_id})".format(tweet_id=tweetDict['id_str'],user_id=tweetDict['user']['id']))
        print(cmd)
        client.command(cmd)

    return ("Tweet added to DB")

#Metodo para realizar las relaciones entre tweets
@celery.task
def add_tweets_relations():
    pending_tweets = client.query("select from Tweet where pending = true limit -1")

    for tweetDict in pending_tweets:
        if 'retweeted_status' in tweetDict.oRecordData:
            if tweetDict.oRecordData['retweeted_status'] != None:
                try:
                    cmd = "create edge Retweet from (select from Tweet where id_str = '{retweet}') to (select from Tweet where id_str = '{original}')".format(retweet=tweetDict.oRecordData['id_str'], original=tweetDict.oRecordData['retweeted_status']['id_str'])
                    client.command(cmd)
                except:
                    pass
                try:    
                    cmd = "create edge Retweeted_by from (select from Tweet where id_str = '{original}') to (select from User where id = {user_id})".format(original=tweetDict.oRecordData['retweeted_status']['id_str'], user_id=tweetDict.oRecordData['user']['id'])
                    client.command(cmd)
                except:
                    pass   
        if 'in_reply_to_status_id' in tweetDict.oRecordData:
            if tweetDict.oRecordData['in_reply_to_status_id'] != None:
                try:
                    cmd = "create edge Reply from (select from Tweet where id_str = '{reply_id}') to (select from Tweet where id_str = '{original_id}')".format(reply_id=tweetDict.oRecordData['id_str'], original_id=tweetDict.oRecordData['in_reply_to_status_id_str'])
                    client.command(cmd)
                except:
                    pass
                try:
                    cmd = "create edge Replied_by from (select from Tweet where id_str = '{original_id}') to (select from User where id = {reply_user_id})".format(original_id=tweetDict.oRecordData['in_reply_to_status_id_str'], reply_user_id=tweetDict.oRecordData['user']['id'])
                    client.command(cmd)
                except:
                    pass
        client.command("update Tweet set pending = false where id_str = '{id_str}'".format(id_str=tweetDict.oRecordData['id_str']))

    print(":FIN:")

@celery.task
def add_tweet(tweetJson):
    # Adaptamos el tweet para la DB
    print("Tweet recibido")

    tweetDict = json.loads(tweetJson)
    time = tweetDict['created_at']
    time = datetime.datetime.strptime(time, "%a %b %d %X %z %Y")
    time = mktime(time.timetuple())
    tweetDict['timestamp_ms'] = time

    tweet_topics = ['default']
    if 'topics' in tweetDict:
        tweet_topics = tweetDict['topics']

    tweetInDB = client.query("select id_str from Tweet where id_str = {id}".format(id=tweetDict['id_str']))
    if tweetInDB:
        client.command("update User set depth = 0 where id = {id}".format( id=tweetDict['user']['id']))
        
        relevance = influence_metrics.main_phase(tweetDict, tweet_topics[0])
        return ("Tweet already in DB. The tweet relevance is {relevance} in the topic {topic}".format(topic=tweet_topics[0],relevance=relevance))

    tweetDict['topics'] = tweet_topics
    logger.warning(tweetDict['topics'])
    tweetJson = json.dumps(tweetDict, ensure_ascii=False).encode().decode('ascii', errors='ignore')
    try:
        cmd = "insert into Tweet content {tweetJson}".format(tweetJson=tweetJson)
        # logger.warning(cmd)
        client.command(cmd)
    except pyorient.exceptions.PyOrientORecordDuplicatedException:
        print ("Tweet already in DB")


    #Relacion con topic
    
    for topic in tweet_topics:
        topicInDB = client.query("select from Topic where name = '{topic}'".format(topic=topic))
        if not topicInDB:
            num_topics = client.query("select count(*) from Topic")[0].oRecordData['count']
            cmd = "insert into Topic set name = '{topic}', id = {id}, tweet_count = 0, user_count = 0".format(topic=topic, id=num_topics)
            logger.warning(cmd)
            client.command(cmd)

        cmd = "create Edge Belongs_to_topic from (select from Tweet where id_str = {tweet_id}) to (select from Topic where name = '{topic}')".format(tweet_id=tweetDict['id_str'], topic=topic)
        logger.warning(cmd)
        client.command(cmd)



    # Comprobamos que su usuario esta en la DB, y si no lo creamos, y lo enlazamos
    if 'user' in tweetDict: 
        user_id = tweetDict['user']['id']
        print("USER ID: " + str(user_id))
        print("TWEET ID: " + str(tweetDict['id']))
        user = []
        try:
            user = client.query("select from User where id = {id}".format(id=user_id))
        except:
            pass
        if not user:
            #print ("No user")
            user_content = tweetDict['user']
            user_content['topics'] = tweet_topics
            user_content['depth'] = 0
            if user_content['following'] == None:
                user_content['following'] = 0
            if user_content['followers_count'] == None:
                user_content['followers_count'] = 0        
            if user_content['friends_count'] == None:
                user_content['friends_count'] = 0
            if user_content['statuses_count'] == None:
                user_content['statuses_count'] = 0
            for key, value in user_content.items():
                if value==None:
                    user_content[key]=""
            cmd = "insert into User content {content}".format(content=user_content)
            #logger.warning(cmd)
            client.command(cmd)
            cmd = "update User set pending = True, depth = 0 where id = {id}".format(id= user_id)
            #logger.warning(cmd)
            client.command(cmd)
            ts = int(tweetDict['timestamp_ms'])/1000
            date_ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            cmd = "insert into User_metrics set id = {id}, lastMetrics = True, topic='{topic}', followers = {followers}, following = {following}, date = '{date}', statuses_count = {statuses_count}, timestamp = {timestamp}, tweetRatio = 0, influence = 0, influenceUnnormalized = 0, voice = 0, voice_r = 0, impact = 0, relevance = 0, complete = False".format(id=user_id,followers=tweetDict['user']['followers_count'],topic=topic,following=tweetDict['user']['friends_count'], date = date_ts, timestamp = ts, statuses_count=tweetDict['user']['statuses_count'])
            #logger.warning(cmd)
            client.command(cmd)
            print("user added")

        client.command("create edge Created_by from (select from Tweet where id_str = '{tweet_id}') to (select from User where id = {user_id})".format(tweet_id=tweetDict['id_str'],user_id=user_id))
        
        cmd = "create edge Belongs_to_topic from (select from User where id = {user_id}) to (select from Topic where name = '{topic}')".format(user_id=user_id, topic=topic)
        client.command(cmd)

    # Creamos una metricas de usuario básicas
    
    # ts = tweetDict['created_at']
    # date_ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweetDict['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))        

    # Comprobamos si el Tweet es un retweet, y lo enlazamos con el original
    if 'retweeted_status' in tweetDict:
        time = tweetDict['retweeted_status']['created_at']
        time = datetime.datetime.strptime(time, "%a %b %d %X %z %Y")
        time = mktime(time.timetuple())
        tweetDict['retweeted_status']['timestamp_ms'] = time
        print("retweeted_status")
        original_tweet = []
        try:
            original_tweet = client.query("select from Tweet where id_str = {id_original}".format(id_original=tweetDict['retweeted_status']['id']))
            
        except:
            pass
            logger.info("El tweet original no se encuentra en la base de datos")

        # Si el tweet original no está en la base de datos, lo creamos, junto con su usuario
        if not original_tweet:
            original_tweet_dict = tweetDict['retweeted_status']
            original_tweet_dict['topics'] = tweet_topics
            original_tweet_dict['user']['screen_name'] = original_tweet_dict['user']['screen_name'].lower()
            original_tweet = json.dumps(original_tweet_dict, ensure_ascii=False).encode().decode('ascii', errors='ignore')
            try:
                cmd = "insert into Tweet content {original_tweet}".format(original_tweet = original_tweet)
                client.command(cmd)
            except pyorient.exceptions.PyOrientORecordDuplicatedException:
                print ("Tweet already in DB")
            user = []
            try:
                user = client.query("select from User where id = {id}".format(id=original_tweet_dict['user']['id']))
            except:
                pass
            if not user:
                original_user_content = original_tweet_dict['user']
                original_user_content['topics'] = tweet_topics
                original_user_content['screen_name'] = original_user_content['screen_name']
                if original_user_content['following'] == None:
                    original_user_content['following'] = 0
                if original_user_content['followers_count'] == None:
                    original_user_content['followers_count'] = 0
                if original_user_content['friends_count'] == None:
                    original_user_content['friends_count'] = 0
                if original_user_content['statuses_count'] == None:
                    original_user_content['statuses_count'] = 0
                for key, value in original_user_content.items():
                    if value==None:
                        original_user_content[key]=""
                cmd = "insert into User content {content}".format(content=original_user_content)
                client.command(cmd)
                cmd = "update User set pending = True, depth = 0 where id = {id}".format(id = original_tweet_dict['user']['id'])
                client.command(cmd)
                print("user added")
                ts = int(tweetDict['retweeted_status']['timestamp_ms'])/1000
                date_ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')                
                client.command("insert into User_metrics set id = {id}, lastMetrics = True, followers = {followers}, following = {following}, date = '{date}', statuses_count = {statuses_count}, tweetRatio = 0, influence = 0, influenceUnnormalized = 0, voice = 0, voice_r = 0, impact = 0, relevance = 0, complete = False".format(id=original_tweet_dict['user']['id'],followers=original_tweet_dict['user']['followers_count'],following=original_tweet_dict['user']['friends_count'], date = date_ts, statuses_count=original_tweet_dict['user']['statuses_count']))
            
            client.command("create edge Created_by from (select from Tweet where id = {tweet_id}) to (select from User where id = {user_id})".format(tweet_id=original_tweet_dict['id'],user_id=original_tweet_dict['user']['id']))
            
            for topic in tweet_topics:
                cmd = "create edge Belongs_to_topic from (select from Tweet where id = {tweet_id}) to (select from Topic where name = '{topic}')".format(tweet_id=original_tweet_dict['id'], topic=topic)
                client.command(cmd)
                cmd = "create edge Belongs_to_topic from (select from User where id = {user_id}) to (select from Topic where name = '{topic}')".format(user_id=original_tweet_dict['user']['id'], topic=topic)
                client.command(cmd)

            # Creamos una metricas de usuario básicas
            #date_ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweetDict['retweeted_status']['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            # print (date_ts)
            #client.command("insert into User_metrics set id = {id}, lastMetrics = True, followers = {followers}, following = {following}, date = '{date}', statuses_count = {statuses_count}, tweetRatio = 0, influence = 0, influenceUnnormalized = 0, voice = 0, voice_r = 0, impact = 0, relevance = 0, complete = False".format(id=original_tweet_dict['user']['id'],followers=original_tweet_dict['user']['followers_count'],following=original_tweet_dict['user']['friends_count'], date = date_ts, statuses_count=original_tweet_dict['user']['statuses_count']))    
            # Planteamos crear el link de last metrics


        # Enlazamos el retweet y el usuario con el original 
        cmd = "create edge Retweet from (select from Tweet where id_str = '{retweet}') to (select from Tweet where id_str = '{original}')".format(retweet=tweetDict['id'], original=tweetDict['retweeted_status']['id'])
        client.command(cmd)
        logger.warning(cmd)
        try:
            cmd = "create edge Retweeted_by from (select from Tweet where id = {original}) to (select from User where id = {user_id})".format(original=tweetDict['retweeted_status']['id'], user_id=tweetDict['user']['id'])
            # logger.warning(cmd)
            client.command(cmd)   
        except:
            pass
        
    # Comprobamos si el Tweet es un reply, y lo enlazamos con el original
    if 'in_reply_to_status_id' in tweetDict:
        print("reply_status")
        original_user = []
        try:
            original_user = client.query("select from User where id = {id_original}".format(id_original=tweetDict['in_reply_to_user_id']))
        except:
            pass

        # Si no esta, creamos el Tweet y el usuario
        if not original_user:
            try:
                cmd = "insert into User set id = {id}, pending = True, depth = 0, topics = {topics}".format(id = tweetDict['in_reply_to_user_id'], topics = tweet_topics)
                client.command(cmd)
            except pyorient.exceptions.PyOrientORecordDuplicatedException:
                print ("Tweet already in DB")
        
        original_tweet = []
        try:
            original_tweet = client.query("select from Tweet where id_str = {id_original}".format(id_original=tweetDict['in_reply_to_status_id']))
        except:
            pass

        # Si no esta, creamos el Tweet
        if not original_tweet:
            try:
                cmd = "insert into Tweet set id = {id}, id_str = {id_str}, topics= {topics}".format(id = tweetDict['in_reply_to_status_id'],id_str = tweetDict['in_reply_to_status_id_str'], topics=tweet_topics)
                client.command(cmd)
                client.command("create edge Created_by from (select from Tweet where id_str = {original_id}) to (select from User where id = {user_id})".format(original_id=tweetDict['in_reply_to_status_id_str'], user_id=tweetDict['in_reply_to_user_id']))
            except pyorient.exceptions.PyOrientORecordDuplicatedException:
                print ("Tweet already in DB")
        # Creamos las relaciones
        logger.info(tweetDict['in_reply_to_status_id'])
        cmd = "create edge Reply from (select from Tweet where id_str = {reply_id}) to (select from Tweet where id_str = {original_id})".format(reply_id=tweetDict['id_str'], original_id=tweetDict['in_reply_to_status_id_str'])
        client.command(cmd)
        cmd = "create edge Replied_by from (select from Tweet where id_str = {original_id}) to (select from User where id = {reply_user_id})".format(original_id=tweetDict['in_reply_to_status_id_str'], reply_user_id=tweetDict['user']['id'])
        client.command(cmd)

            # Los enlazamos con el topic
        for topic in tweet_topics:
            cmd = "create edge Belongs_to_topic from (select from Tweet where id = {tweet_id}) to (select from Topic where name = '{topic}')".format(tweet_id=tweetDict['in_reply_to_status_id'], topic=topic)
            client.command(cmd)
            cmd = "create edge Belongs_to_topic from (select from User where id = {user_id}) to (select from Topic where name = '{topic}')".format(user_id=tweetDict['in_reply_to_user_id'], topic=topic)
            client.command(cmd)
       
    relevance = influence_metrics.main_phase(tweetDict, tweet_topics[0])
    print("Tweet added to DB")
    return ("Tweet added to DB. The tweet relevance is {relevance} in the topic {topic} ".format(topic=tweet_topics[0],relevance=relevance))

@celery.task
def delete_tweet(tweet_id):
    client.command("delete vertex from Tweet where id_str = {id}".format(id=tweet_id))
    return ("Tweet deleted from DB")

@celery.task
def tweet_search(attributes, limit, topic, sort_by):
    # Revisar la forma de hacer la búsqueda
    if topic:
        if sort_by:
            tweet_search = client.query("select {attributes} from Tweet where topics containsText '{topic}' order by {sort_by} limit {limit}".format(attributes=attributes, topic=topic, sort_by=sort_by, limit=limit))
        else:
            tweet_search = client.query("select {attributes} from Tweet where topics containsText '{topic}' limit {limit}".format(attributes=attributes, topic=topic, limit=limit))
    elif sort_by:
        tweet_search = client.query("select {attributes} from Tweet order by {sort_by} limit {limit}".format(attributes=attributes, sort_by=sort_by, limit=limit))
    else:
        tweet_search = client.query("select {attributes} from Tweet limit {limit}".format(attributes=attributes, limit=limit))
    # Procesar los tweets y eliminar los atributos de OrientDB y las metricas viejas
    tweet_list=[]
    for tweet_record in tweet_search:
        tweet = tweet_record.oRecordData
        for k in delete_variables:
            if tweet.get(k):
                del tweet[k]
        tweet_list.append(tweet)
    return tweet_list

@celery.task
def get_tweet_emotion(tweet_id):
    emotionRecord = client.query("select expand(out('hasEmotionSet')) from Tweet where id_str = '{tweet_id}'".format(tweet_id=tweet_id))   
    return emotionRecord[0].oRecordData

@celery.task
def get_tweet_sentiment(tweet_id):
    sentimentRecord = client.query("select expand(out('hasEmotionSet')) from Tweet where id_str = '{tweet_id}'".format(tweet_id=tweet_id))   
    return sentimentRecord[0].oRecordData

@celery.task
def get_tweet_metrics(tweet_id):
    try:
        metricsRecord = client.query("select expand(out('Last_metrics')) from Tweet where id_str = '{tweet_id}'".format(tweet_id=tweet_id))   
        tweet_metrics = metricsRecord[0].oRecordData
        tweet_metrics.pop("in_Last_metrics")
        return tweet_metrics
    except:
        return "Tweet metrics have not been calculated yet"

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
def topic_network(topic_id, entity):
    topicRecord = client.query("select name from Topic where id = {topic_id}".format(topic_id=topic_id))
    topic = topicRecord[0].oRecordData['name']
    print(topic)
    user_topic = client.query("select id_str from {entity} where topics containstext '{topic}' and id_str is not null limit -1".format(topic=topic, entity=entity))
    user_topic_list=[]
    for user_record in user_topic:
        user = user_record.oRecordData
        #print(user)
        user_topic_list.append(user)
    return user_topic_list

#@periodic_task(run_every=timedelta(days=1))
#@periodic_task(run_every=timedelta(minutes=1))
#@periodic_task(run_every=crontab(hour=14, minute=9, day_of_week="wed"))
#@celery.task(base=QueueOnce)
@celery.task(throws=(Terminated,))
def get_users_from_twitter(pending_users=None):
    print("TAREA PERIODICA")
    n_lim = 2
    wq = bitter.crawlers.TwitterQueue.from_credentials('credentials.json')
    if not pending_users:
        limit = 1000
        skip = 0
        depth = 1
        user_count = client.query("select count(*) from User where pending = True and depth < {depth}".format(depth=depth))
        print(user_count)
        number_of_users = user_count[0].oRecordData['count']
        iterations = math.ceil(number_of_users/limit)
        print("numero de iteraciones: {iterations}".format(iterations=iterations))

        for iteration_num in range(0,iterations):
            pending_users = client.query("select id, depth from User where pending = True and depth < {depth} skip {skip} limit {limit}".format(depth=depth, skip=skip, limit=limit))
            pending_user_list = []
            for user in pending_users:
                pending_user_list.append(str(user.oRecordData['id']))
            for user in bitter.utils.get_users(wq,pending_user_list):
                
                user_topics = client.query("select topics from User where id = {id}".format(id=user['id']))[0].oRecordData['topics'] 
                user['topics'] = user_topics
                user_final = json.dumps(user, ensure_ascii=False).encode().decode('ascii', errors='ignore')
                logger.warning(user['id'])

                cmd = "update User content {user} where id = {id}".format(user=user_final, id=user['id'])
                # logger.warning(cmd)
                client.command(cmd)
                client.command("update User set pending = False, depth = 0 where id = {id}".format(id=user['id']))
                print("Usuario actualizado")

                #Creamos una metrica nueva
                ts = time.time()
                date_ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                for topic in user_topics:
                    client.command("insert into User_metrics set id = {id}, lastMetrics = True, topic = '{topic}', followers = {followers}, following = {following}, date = '{date}', statuses_count = {statuses_count}, timestamp = {timestamp}, tweetRatio = 0, influence = 0, influenceUnnormalized = 0, voice = 0, voice_r = 0, impact = 0, relevance = 0, complete = False".format(id=user['id'],followers=user['followers_count'],following=user['friends_count'], topic= topic, date = date_ts, timestamp = ts, statuses_count = user['statuses_count']))    
                
                # RELACION FOLLOW
                pending = True
                cursor = -1
                limitator = 0
                print("Empieza la descarga de usuarios de {id}".format(id=user['id']))
                while pending:
                    try:
                        resp = wq.followers.ids(user_id=user['id'], cursor=cursor)
                    except TwitterHTTPError as ex:
                        # if ex.e.code in (401, ):
                        break
                    except:
                        print ("Exception")
                        #logger.info('Not authorized for user: {}'.format(user['id']))
                        break
                        #resp = {}
                    # logger.warning(resp)
                    print("Usuarios descargados")

                    if 'ids' in resp:
                        limitator +=1
                        for follower in resp['ids']:
                            #print ("esto es lo que da problemas: {follower}".format(follower=follower))
                            follower_user=[]
                            follower_user = client.query("select id from User where id = {id}".format(id=follower))

                            #if not follower_user:
                            #    user_content ={'id': follower, 'depth': 2, 'pending': False, 'topics': user_topics}
                            #    user_content_json = json.dumps(user_content, ensure_ascii=False).encode().decode('ascii', errors='ignore')
                            #    cmd = "insert into User content {content}".format(content=user_content_json)
                                #cmd = "insert into User set id = {id}, depth = {user_depth}, pending = True, topics={topics}".format(id=follower, user_depth = 1, topics=topics_json)
                                # logger.warning(cmd)
                            #    client.command(cmd)
                                #print("user added")
                            if follower_user:
                                cmd = "create edge Follows from (select from User where id = {follower_id}) to (select from User where id = {user_id})".format(follower_id=follower, user_id=user['id'])
                                # logger.warning(cmd)
                                client.command(cmd)
                            #for topic in user_topics:
                            #    cmd = "create edge Belongs_to_topic from (select from User where id = {follower_id}) to (select from Topic where name = '{topic}')".format(follower_id=follower, topic=topic)
                            #    client.command(cmd)


                        cursor = resp["next_cursor"]
                        print ("Cursor: {cursor}".format(cursor=cursor))
                        if cursor > 0 and limitator < n_lim:
                            logger.info("Getting more followers for %s" % user['id'])
                        else:
                            logger.info("Done getting followers for %s" % user['id'])
                            cursor = -1
                            pending = False
                    else:
                        pass

            skip += limit
    #get_detailed_users_from_twitter()
    print ("SUCCESS")
    return "Users updated"

#Tarea periódica que descarga los detalles de los usuarios de twitter incompletos
#@celery.task()
#@periodic_task(run_every=crontab(hour=13, minute=44, day_of_week="wed"))
#@celery.task(base=QueueOnce)
#@periodic_task(run_every=timedelta(minutes=20))
def get_detailed_users_from_twitter(pending_users=None):
    print("TAREA DETALLES USUARIOS")
    wq = bitter.crawlers.TwitterQueue.from_credentials('credentials.json')
    if not pending_users:
        limit = 10000
        skip = 0
        depth = 2

        number_of_users = client.query("select count(*) from User where pending = false and screen_name is null".format(depth=depth))[0].oRecordData['count']
        iterations = math.ceil(number_of_users/limit)
        print("numero de iteraciones: {iterations}".format(iterations=iterations))

        for iteration_num in range(0,iterations):
            pending_users = client.query("select id, depth from User where pending = false and screen_name is null and depth <= {depth} skip {skip} limit {limit}".format(depth=depth, skip=skip, limit=limit))
            pending_user_list = []
            for user in pending_users:
                pending_user_list.append(str(user.oRecordData['id']))
            for user in bitter.utils.get_users(wq,pending_user_list):
                user_topics = client.query("select topics from User where id = {id}".format(id=user['id']))[0].oRecordData['topics'] 
                user['topics'] = user_topics
                user_final = json.dumps(user, ensure_ascii=False).encode().decode('ascii', errors='ignore')
                logger.warning(user['id'])
                cmd = "update User content {user} and depth = 2 where id = {id}".format(user=user_final, id=user['id'])
                # logger.warning(cmd)
                client.command(cmd)
                print("Usuario actualizado")

                #Creamos una metrica nueva
                ts = time.time()
                date_ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                for topic in user_topics:
                    client.command("insert into User_metrics set id = {id}, lastMetrics = True, topic = '{topic}', followers = {followers}, following = {following}, date = '{date}', statuses_count = {statuses_count}, timestamp = {timestamp}, tweetRatio = 0, influence = 0, influenceUnnormalized = 0, voice = 0, voice_r = 0, impact = 0, relevance = 0, complete = False".format(id=user['id'],followers=user['followers_count'],following=user['friends_count'], topic= topic, date = date_ts, timestamp = ts, statuses_count = user['statuses_count']))    

            skip += limit
    print ("SUCCESS")

@celery.task()
def get_tweets_by_id(pending_tweets=None):
    wq = bitter.crawlers.TwitterQueue.from_credentials('credentials.json')
    if not pending_tweets:
        limit = 100
        skip = 0
        number_of_tweets = client.query("select count(*) from Tweet where pending = True ")[0].oRecordData['count']
        pending_tweets_total = []
        while number_of_tweets > 0:    
            logger.info(" %s tweets remaining" % number_of_tweets)
            ids = ""
            pending_tweets = client.query("select id_str from Tweet where pending = True limit {limit}".format(limit=limit))
            
            pending_tweets_list = []
            
            for tweet in pending_tweets:
                pending_tweets_list.append(str(tweet.oRecordData['id_str']))
            for tweet in pending_tweets_list:
                if tweet not in pending_tweets_total:
                    if tweet == pending_tweets_list[len(pending_tweets_list)-1]:
                        ids += tweet
                    else:
                        ids += tweet + ","
                    pending_tweets_total.append(str(tweet))

                else:
                    cmd = "update tweet set pending = false where id_str = {id_str}".format(id_str=tweet)
                    client.command(cmd)
            if ids:
                for tweet in wq.statuses.lookup(_id=ids):
                    tweet_topics = client.query("select topics from tweet where id_str = {id_str}".format(id_str=tweet['id_str']))[0].oRecordData['topics'] 
                    tweet['topics'] = tweet_topics
                    tweet['pending'] = False
                    time = tweet['created_at']
                    time = datetime.datetime.strptime(time, "%a %b %d %X %z %Y")
                    time = mktime(time.timetuple())
                    tweet['timestamp_ms'] = time
                    reply_variables = ['in_reply_to_user_id','in_reply_to_status_id','in_reply_to_user_id_str','in_reply_to_status_id_str','in_reply_to_screen_name']
                    for k in reply_variables:
                        if not tweet.get(k):
                            del tweet[k]
                    tweet_json = json.dumps(tweet, ensure_ascii=False).encode().decode('ascii', errors='ignore')
                    cmd = "delete vertex from Tweet where id_str = {id_str}".format(id_str=tweet['id_str'])
                    client.command(cmd)
                    add_tweet(tweet_json)
            number_of_tweets = client.query("select count(*) from Tweet where pending = True")[0].oRecordData['count']
    logger.info("TWEETS HYDRATED")

@celery.task
def get_task_list():
    i = inspect()
    return i.active()
    #return i.registered_tasks()
    #return i.scheduled()
    
@celery.task
def get_task_status(taskId):
    res = AsyncResult(taskId)
    status = "Unknown"
    if str(res.ready())=="False":
        status = "Pending"
    elif str(res.ready())=="True":
        status = "Finished"
    return status

#@periodic_task(run_every=crontab(hour=10, minute=40, day_of_week="thu"))
@celery.task(throws=(Terminated,))
def execute_metrics():
    print("COMIENZAN LAS METRICAS")
    influence_metrics.execution()
    return "Metrics calculated"


@celery.task
def execute_communities():
    logger.info("COMIENZAN LAS METRICAS")
    compute_communities.execution()
# @celery.task
# def get_user_of_tweet(tweetId):
#     wq = bitter.crawlers.TwitterQueue.from_credentials('credentials.json')
#     # pending_user = client.query("select user.id from Tweet where id = {tweetId}".format(tweetId=tweetId))
#     # logger.error(pending_user[0].oRecordData)
#     # pending_user_list = [pending_user[0].oRecordData['id']]
#     pending_user_list = ["88602264",]
#     users_retrieved = bitter.utils.get_users(wq,pending_user_list)
#     for user_extracted in users_retrieved:
#         user_final = json.dumps(user_extracted, ensure_ascii=False).encode().decode('ascii', errors='ignore')
#         logger.error(user_final)
#         client.command("insert into User content {user}".format(user=user_final))
#     return "SUCCESS"


#@celery.task
#def add_new_emotion(emotion):
	

#get_users_from_twitter.delay()
#execute_metrics()
#@periodic_task(run_every=crontab(hour=11, minute=4))
@celery.task
def get_emotions_from_tweets():
    tweets = client.command("select from tweet")
    # Adding emotions to DB 
    for tweet_record in tweets:
        tweet = tweet_record.oRecordData
        emotionSetInDB = client.query("select expand(out('hasEmotionSet')) from Tweet where id_str = '{tweet_id}'".format(tweet_id=tweet['id_str']))
        if not emotionSetInDB:
            r = requests.get('http://senpy.cluster.gsi.dit.upm.es/api/?algo=EmoTextANEW&lang=es&i=%s' % tweet["text"])
            response = r.content.decode('utf-8')
            response_json = json.loads(response)
            text = response_json["entries"][0]["nif:isString"].replace("'","\"")
            arousal = response_json["entries"][0]["emotions"][0]["onyx:hasEmotion"][0]["http://www.gsi.dit.upm.es/ontologies/onyx/vocabularies/anew/ns#arousal"]
            dominance = response_json["entries"][0]["emotions"][0]["onyx:hasEmotion"][0]["http://www.gsi.dit.upm.es/ontologies/onyx/vocabularies/anew/ns#dominance"]
            valence = response_json["entries"][0]["emotions"][0]["onyx:hasEmotion"][0]["http://www.gsi.dit.upm.es/ontologies/onyx/vocabularies/anew/ns#valence"]
            hasEmotionCategory = response_json["entries"][0]["emotions"][0]["onyx:hasEmotion"][0]["onyx:hasEmotionCategory"]
            add_new_emotion(hasEmotionCategory)
            emo_id = int(response_json["entries"][0]["@id"].split("_")[-1].replace(".",""))
            onyx_hasEmotion = {"http://www.gsi.dit.upm.es/ontologies/onyx/vocabularies/anew/ns#arousal":arousal,"http://www.gsi.dit.upm.es/ontologies/onyx/vocabularies/anew/ns#dominance":dominance,"http://www.gsi.dit.upm.es/ontologies/onyx/vocabularies/anew/ns#valence":valence,"onyx:hasEmotionCategory":hasEmotionCategory}
            onyx_hasEmotion_json = json.dumps(onyx_hasEmotion, ensure_ascii=False).encode().decode('ascii', errors='ignore')
            try:
                cmd = "insert into EmotionSet set nif__isString = '{text}', id = {id}, onyx__hasEmotion = {onyx}".format(text=text, id=emo_id, onyx=onyx_hasEmotion_json)
                logger.warning(cmd)
                client.command(cmd)
            except:
                print("Tweet inválido para analizar emociones")
            try:
                cmd = "create Edge hasEmotionSet from (select from Tweet where id_str = '{tweet_id}') to (select from EmotionSet where id = '{emotion_id}')".format(tweet_id = tweet['id_str'],emotion_id = emo_id)
                logger.warning(cmd)
                client.command(cmd)
            except:
                print("No se ha podido enlazar la emocion con el tweet")
        else:    
        	print("Emociones ya calculadas para este tweet")    
    print("Finish Task")

@celery.task
def get_communities_list():
    communities = client.query("select from community limit -1")
    community_list = []
    for community in communities:
        community = community.oRecordData
        community.pop("in_Belongs_to_Community", None)
        community.pop("out_Belongs_to_topic", None)
        community_list.append(community)
    return community_list

@celery.task
def get_community_network(communityId):
    user_list = client.query("select expand(in('Belongs_to_Community')) from community where id = {community_id} limit -1".format(community_id=communityId))
    user_community_list=[]
    for user_record in user_list:
        user = user_record.oRecordData
        for k in delete_variables:
            if user.get(k):
                del user[k]
        #print(user)
        user_community_list.append(user)
    return user_community_list

@celery.task
def get_community(communityId):
    communityRecord = client.query("select from community where id = {community_id}".format(community_id=communityId))
    community = communityRecord[0].oRecordData
    community.pop("in_Belongs_to_Community", None)
    return community

@celery.task
def get_sentiments_from_tweets():
    tweets = client.command("select from tweet where polarityValue is null limit -1")
    for tweet_record in tweets:
        tweet = tweet_record.oRecordData
        r = requests.get('http://senpy.cluster.gsi.dit.upm.es/api/?algo=sentiText&lang={lang}&i={text}'.format(text=tweet["text"], lang=tweet["lang"]))
        response = r.content.decode('utf-8')
        response_json = json.loads(response)
        polarity = response_json["entries"][0]["sentiments"][0]["marl:polarityValue"] 
        try:
            client.command('update Tweet set polarityValue={polarity} where id={id}'.format(polarity=polarity, id=tweet['id_str']))
        except:
            print("No se ha podido calcular el sentimento del tweet")    
    print("Finish Task")

@celery.task
def calculate_user_sentiment():
    users = client.command("select from user where polarityValue is null limit -1")
    for user_record in users:
        user = user_record.oRecordData
        polarities = client.query("select polarityValue from (select expand(in('Created_by')) from user where id = {userId} limit -1) limit -1".format(userId=user['id_str']))
        sum_polarity = 0
        for polarity in polarities:
            try:
                #print(polarity.oRecordData)
                sum_polarity += polarity.oRecordData['polarityValue']
            except:
                print("El tweet no tiene sentimiento calculado")
        med_polarity = sum_polarity/len(polarities)
        try:
            client.command("update User set polarityValue = {polarity} where id={id}".format(polarity=med_polarity, id=user['id_str']))
        except:
            print("No se ha podido calcular el sentimiento para el usuario")
    print("Task Finished")

@celery.task
def calculate_community_sentiment():
    communities = client.command("select from community where polarityValue is null limit -1")
    for community_record in communities:
        community = community_record.oRecordData
        polarities = client.query("select polarityValue from (select expand(in('Belongs_to_community')) from community where id = {communityid} limit -1) limit -1".format(communityid=community['id']))
        sum_polarity = 0
        for polarity in polarities:
            try:
                sum_polarity += polarity.oRecordData['polarityValue']
                print(polarity.oRecordData)
            except:
                print("El usuario de la comunidad no tiene sentimiento calculado")
        print(sum_polarity)
        med_polarity = sum_polarity/len(polarities)
        print(med_polarity)
        try:
            client.command("update community set polarityValue = {polarity} where id={id}".format(polarity=med_polarity, id=community['id']))
        except:
            print("No se ha podido calcular el sentimiento para la community")
    print("Task Finished")

@celery.task
def get_community_sentiment(communityId):
    communityRecord = client.query("select from community where id = {community_id}".format(community_id=communityId))
    community = communityRecord[0].oRecordData
    community.pop("in_Belongs_to_Community", None)
    if community['polarityValue'] > 0.25:
        community['polarity'] = "positive"
    if community['polarityValue'] < -0.25:
        community['polarity'] = "negative"
    if community['polarityValue'] < 0.25 and community['polarityValue'] > -0.25:
        community['polarity'] = "neutral"
    return community


