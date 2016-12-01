import pyorient
import math
import numpy as np
import time
import datetime
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix
import gc
import os
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

#CONFIGURACIÓN PARA DOCKER
ORIENTDB_HOST = os.environ.get('ORIENTDB_HOST')

if ORIENTDB_HOST != None:
    client = pyorient.OrientDB(ORIENTDB_HOST, 2424)
    session_id = client.connect("root", "root")
    client.db_open("mixedemotions", "admin", "admin")
else: 
    client = pyorient.OrientDB("orientdb_test", 2424)
    session_id = client.connect("root", "root")
    client.db_open("mixedemotions", "admin", "admin")

#CONFIGURACION PARA LOCAL
# client = pyorient.OrientDB("localhost", 2424)
# session_id = client.connect("root", "root")
# client.db_open("mixedemotions", "admin", "admin")

# FALTA TENER EL NÚMERO TOTAL DE TWEETS DE UN USUARIO FUERA DE LA BUSQUEDA
# Metodo para calcular la metrica TR SCORE de todos los usuarios
def user_tweetratio_score(userlist, topic):
    print("USER TWEETRATIO")
    IS_TEST = os.environ.get('IS_TEST')
    if IS_TEST:
        print ("Testing...")
        test_metrics = {}
    # userlist = client.query("select from User limit -1")
    for user in userlist:
        user_metrics_list = client.query("select from User_metrics where topic = '{topic}' and id = {id} order by timestamp desc".format(id = user.oRecordData['id'], topic=topic))
        tweets_from_user_in_DB = client.query("select count(*) from (select expand(in('Created_by')) from User where id = {id} limit -1) where topics containsText '{topic}' limit -1".format(id = user.oRecordData['id'], topic=topic))

        if len(user_metrics_list) > 1:
            tweet_difference = user_metrics_list[0].oRecordData['statuses_count'] - user_metrics_list[-1].oRecordData['statuses_count']
            if tweet_difference == 0:
                tweet_ratio = tweets_from_user_in_DB[0].oRecordData['count'] / user_metrics_list[0].oRecordData['statuses_count']
            else:
                tweet_ratio = tweets_from_user_in_DB[0].oRecordData['count'] / tweet_difference
        else:
            tweet_ratio = tweets_from_user_in_DB[0].oRecordData['count'] / user_metrics_list[0].oRecordData['statuses_count']

        tweet_ratio = abs(tweet_ratio)
        tweet_ratio = truncate(tweet_ratio, 12)
        if IS_TEST:
            screen_name = client.query("select screen_name from user where id = {id}".format(id=user.oRecordData['id']))
            test_metrics[screen_name[0].oRecordData['screen_name']] = tweet_ratio
        # CREAMOS EL OBJETO DE METRICAS DE USUARIO
        user_metrics_object_creation(user, tweet_ratio, topic)

    if IS_TEST:
        return test_metrics
    print("METRICAS CREADAS")

        # tweets_related_user = client.query("select from Tweet where user_id = '{userid}'".format(userid=user.oRecorData['id']) )
        # tweets_related_user = len(tweets_related_user)
        # tweets_total_user = int(user.oRecordData['total_tweets'])
        # TR_score = tweets_related_user/tweets_total_user
        # command = "update (select from User where id = {id}) set metrics.TR_score = {TR_score}".format(id=user.oRecordData['id'], TR_score=TR_score)
        # #command = "update (select from User where id = '" + str(user.oRecordData['userid']) + "') set TR_score = '" + str(0.5) + "'"
        # client.command(command)


# Metodo para calcular la metrica UI SCORE
def influence_score(userlist, number_of_users, number_of_tweets, topic):
    print("INFLUENCE SCORE")
    IS_TEST = os.environ.get('IS_TEST')
    if IS_TEST:
        print ("Testing...")
        influence_score = {}
    # Parametros
    limit = 10000
    iterationRID = "#-1:-1"
    index = 0
    # Parámetro de Noro
    s = 0.1
    # iterations = max([(number_of_users/limit), (number_of_tweets/limit)])
    iterations = math.ceil(number_of_tweets/limit)
    print("numero de iteraciones: {iterations}".format(iterations=iterations))

    # Creamos las matrices At, Ar y As vacia
    At = lil_matrix((number_of_tweets,number_of_users))
    Ar = lil_matrix((number_of_users,number_of_tweets))
    As = lil_matrix((number_of_users,number_of_tweets))

    # userlist = client.query("select from User order by metrics.followers desc limit 500")
    # userlist = client.query("select from User limit -1")
    print("COMIENZO A CALCULAR")
    for iteration_num in range(0,iterations):
        tweetlist = client.query("select id_str from Tweet where @rid > {iterationRID} and topics containsText '{topic}' and retweeted_status is null limit {limit}".format(iterationRID=iterationRID, topic=topic, limit=limit))

        # Iteramos los usuarios y los tweets para rellenar las matrices
        index_start = index
        for n,user in enumerate(userlist):

            # Creamos el vector para la matriz At
            user_tweet_At = np.array([])
            # Creamos el vector para la matriz Ar
            tweet_user_Ar = np.array([])
            # Creamos el vector para la matriz As (FALTA PARAMETRO s)
            user_user_As = np.array([])

            # PUEDO OPTIMIZAR METIENDO ESTAS QUERYS EN LOS IF DE DEBAJO
            # PLANTEAR METER (in('Created_by').id) para optimizar > Cambiar ['id'] por value

            user_created = client.query("select from (select expand(in('Created_by')) from User where id = {user_id} limit -1) where topics containsText '{topic}' and retweeted_status is null limit -1".format(user_id=user.oRecordData['id'], topic = topic))
            
            user_retweeted = client.query("select from (select expand(in('Retweeted_by')) from User where id = {user_id} limit -1) where topics containsText '{topic}' and retweeted_status is null limit -1".format(user_id=user.oRecordData['id'], topic=topic))

            user_replied = client.query("select from (select expand(in('Replied_by')) from User where id ={user_id} limit -1) where topics containsText '{topic}' limit -1".format(user_id=user.oRecordData['id'], topic=topic))

            user_follows_created = client.query("select from (select expand(out('Follows').in('Created_by')) from User where id = {user_id} limit -1) where topics containsText '{topic}' and retweeted_status is null limit -1".format(user_id=user.oRecordData['id'], topic=topic))
      
            user_follows_retweeted = client.query("select from (select expand(out('Follows').in('Retweeted_by')) from User where id ={user_id} limit -1) where topics containsText '{topic}' limit -1".format(user_id=user.oRecordData['id'], topic=topic))

            
            for tweet in tweetlist:
                found_At = False
                found_Ar = False
                found_As = False

                # Calculamos el vector para At y para Ar
                for retweeted in user_retweeted:
                    if retweeted.oRecordData['id_str'] == tweet.oRecordData['id_str']:
                        user_tweet_At = np.append(user_tweet_At, np.ones(1))
                        found_At = True
                        tweet_user_Ar = np.append(tweet_user_Ar, np.ones(1))
                        found_Ar = True
                        break

                if not found_At:        
                    for created in user_created:
                        if created.oRecordData['id_str'] == tweet.oRecordData['id_str']:
                            user_tweet_At = np.append(user_tweet_At, np.ones(1))
                            found_At = True
                            break

                if not found_Ar:
                    for replied in user_replied:
                        if replied.oRecordData['id_str'] == tweet.oRecordData['id_str']:
                            tweet_user_Ar = np.append(tweet_user_Ar, np.ones(1))
                            found_Ar = True
                            break 

                # Calculamos el vector para As
                for tweet_follow in user_follows_created:
                    if tweet_follow.oRecordData['id_str'] == tweet.oRecordData['id_str']:
                        user_user_As = np.append(user_user_As, np.ones(1))
                        found_As = True
                        break
                if not found_As:
                    for retweet_follow in user_follows_retweeted:
                        if retweet_follow.oRecordData['id_str'] == tweet.oRecordData['id_str']:
                            user_user_As = np.append(user_user_As, np.ones(1))
                            found_As = True
                            break

                if not found_As:
                    user_user_As = np.append(user_user_As,np.zeros(1)*s)
                if not found_At:
                    user_tweet_At = np.append(user_tweet_At, np.zeros(1))
                if not found_Ar:
                    tweet_user_Ar = np.append(tweet_user_Ar,np.zeros(1))
                    
            # At[index_start:index,n] = user_tweet_At
            # Ar[n,index_start:index] = tweet_user_Ar
            # As[n,index_start:index] = user_user_As

            arrayindex = index_start

            if arrayindex < (number_of_tweets-(limit+5000)):
                for element in user_tweet_At:                
                    At[arrayindex,n] = element
                    arrayindex +=1
                arrayindex = index_start
                for element in tweet_user_Ar:                
                    Ar[n,arrayindex] = element
                    arrayindex +=1
                arrayindex = index_start
                for element in user_user_As:
                    As[n,arrayindex] = element
                    arrayindex +=1
            else:
                for element in user_tweet_At:                
                    At[arrayindex,n] = element
                    arrayindex +=1
                    if arrayindex > number_of_tweets:
                        break
                arrayindex = index_start
                for element in tweet_user_Ar:                
                    Ar[n,arrayindex] = element
                    arrayindex +=1
                    if arrayindex > number_of_tweets:
                        break
                arrayindex = index_start
                for element in user_user_As:
                    As[n,arrayindex] = element
                    arrayindex +=1
                    if arrayindex > number_of_tweets:
                        break


        #CONSEGUIR OBTENER RID
        index += 10000 
        iterationRID = tweet._rid
        print("Fin de iteracion {iteration_num}".format(iteration_num=iteration_num+1))


    # DAMPING FACTOR
    d = 0.15

    Ar = csr_matrix(Ar)
    At = csr_matrix(At)
    As = csr_matrix(As)
   
    # Creamos la matriz Bt:
    Bt = lil_matrix((number_of_tweets,number_of_users))
    n_filas_At = At.shape[0]
    n_columnas_At = At.shape[1]
    for i in range(0, n_filas_At):
        sumatorio_At = At[i].sum()
        if sumatorio_At != 0:
            for j in range(0,n_columnas_At):
                Bt[i,j] = At[i,j]/sumatorio_At
        else:
            for j in range(0,n_columnas_At):
                Bt[i,j] = 0

    Bt = csr_matrix(Bt)
    # LIMPIAMOS MEMORIA
    At = 0
    gc.collect()

    # Creamos la matriz Ba
    Ba = lil_matrix((number_of_users,number_of_tweets))
    n_filas_Ar = Ar.shape[0]
    n_columnas_Ar = Ar.shape[1]

    for i in range(0, n_filas_Ar):
        sumatorio_Ar = Ar[i].sum()
        sumatorio_As = As[i].sum()
        if sumatorio_As != 0:
            if sumatorio_Ar == 0:
                for j in range(0,n_columnas_Ar):
                    Ba[i,j] = As[i,j]/sumatorio_As
            else:
                for j in range(0,n_columnas_Ar):
                    Ba[i,j] = (Ar[i,j]/sumatorio_Ar)*(1-d) + (As[i,j]/sumatorio_As)*d
        else:
            for j in range(0,n_columnas_Ar):
                Ba[i,j] = 0
    
    Ba = csr_matrix(Ba)

    # LIMPIAMOS MEMORIA
    Ar = 0
    As = 0
    gc.collect()

    # Calculamos UI y TI
    users_vector = np.ones((number_of_users))/number_of_users
    tweets_vector =  np.ones((number_of_tweets))/number_of_tweets

    Ba_transpose = Ba.transpose()
    Bt_transpose = Bt.transpose()

    # # LIMPIAMOS MEMORIA
    Ba = 0
    Bt = 0
    gc.collect()

    for k in range(1, 15):
        tweets_vector = Ba_transpose.dot(users_vector)
        users_vector = Bt_transpose.dot(tweets_vector)

    # LIMPIAMOS MEMORIA
    Ba_transpose = 0
    Bt_transpose = 0
    gc.collect()

    # Normalizamos UI y TI
    try:
        UI_vector = users_vector/np.amax(users_vector)
        TI_vector = tweets_vector/np.amax(tweets_vector)
    except:
        logger.warning("USUARIOS NO RELACIONADOS")


    #ALMACENAMOS EN LA DB LAS PUNTUACIONES
    for n,user in enumerate(userlist):
        
        UI = UI_vector[n]
        
        UI_unnormalized = users_vector[n]
        UI = truncate(UI, 10)
        UI_unnormalized = truncate(UI_unnormalized, 12)

        # if UI_unnormalized < 0.0000999:
        #     UI_unnormalized = 0
        # if UI < 0.0000999:
        #     UI = 0.0001
        if IS_TEST:
            screen_name = client.query("select screen_name from user where id = {id}".format(id=user.oRecordData['id']))
            influence_score[screen_name[0].oRecordData['screen_name']] = UI_unnormalized

        command = "update User_metrics set influence={UI_score}, influenceUnnormalized={UI_unnormalized} where id={user_id} and lastMetrics = True and topic = '{topic}'".format(user_id=user.oRecordData['id'], UI_score=UI, UI_unnormalized=UI_unnormalized, topic=topic)
        #print (command)
        client.command(command)

    newindex = 0
    iterationRID = "#-1:-1"
    for iteration_num in range(0,iterations):
        tweetlist = client.query("select id from Tweet where @rid > {iterationRID} and topics containsText '{topic}' and retweeted_status is null limit {limit}".format(iterationRID=iterationRID, topic=topic, limit=limit))

        for n,tweet in enumerate(tweetlist):

            # CREAMOS EL OBJETO DE METRICAS TWEET Y LO RELLENAMOS
            tweet_metrics_object_creation(tweet, topic)
            TI_score = TI_vector[n+newindex]
            TI_score = truncate(TI_score, 12)

            # if TI_score < 0.0000999:
            #     TI_score = 0.0001
            if IS_TEST:
                influence_score[tweet.oRecordData['id']] = TI_score

            command = "update Tweet_metrics set influence = {TI_score} where id = {id} and lastMetrics = True and topic = '{topic}'".format(id=tweet.oRecordData['id'], TI_score=TI_score, topic=topic)
            client.command(command)
        newindex += 10000 
        iterationRID = tweet._rid
    if IS_TEST:
        return influence_score
    print("FIN influence_score")

    # while (error_u > 0.1) or (error_t > 0.1):
    #     error_u = -np.mod(users_vector)
    #     error_t = -np.mod(tweets_vector)
    #     tweets_vector = np.dot(Ba.transpose(), users_vector)
    #     users_vector = np.dot(Bt.transpose(), tweets_vector)
    #     error_u += np.mod(users_vector)
    #     error_t += np.mod(tweets_vector)

    
def follow_relation_factor_user(userlist, number_of_users, topic):
    print("FOLLOW RELATION FACTOR USER")
    IS_TEST = os.environ.get('IS_TEST')
    if IS_TEST:
        print ("Testing...")
        follow_relation_score = {}
    # userlist = client.query("select from User order by metrics.followers desc limit 500")
    # userlist = client.query("select from User limit -1")

    Af = np.zeros((number_of_users, number_of_users))

    for n, user in enumerate(userlist):
        user_user_Af = np.array([])

        # PLANTEAR METER (in('Created_by').id) para optimizar > Cambiar ['id'] por value

        user_follows = client.query("select from (select expand(out('Follows')) from User where id = {id} limit -1) where topics containsText '{topic}' limit -1".format(id=user.oRecordData['id'], topic=topic))
        
        for user_2 in userlist:
            found_Af = False

            for follow in user_follows:
                if (user_2.oRecordData['id'] == follow.oRecordData['id']):
                    user_user_Af = np.append(user_user_Af, np.ones(1))
                    found_Af = True
                    break
            if not found_Af:
                user_user_Af = np.append(user_user_Af,np.zeros(1))

        Af[n,:] = user_user_Af

    # DAMPING FACTOR
    d = 0.15

    # Creamos la matriz de adyacencia Bf
    Bf = np.zeros((number_of_users, number_of_users))
    n_users = Af.shape[0]
    for n in range(0, n_users):
        sumatorio_Af = Af[n].sum()
        Bf_row = np.ones(n_users)
        if sumatorio_Af == 0:
            Bf_row = Bf_row/n_users
        else:
            Bf_row = (Af[n]/sumatorio_Af)*(1-d) + d/n_users

        Bf[n,:] = Bf_row

    # Calculamos FR
    follow_vector = np.ones((number_of_users))/number_of_users
    
    for k in range(1, 1000):
        follow_vector = np.dot(Bf.transpose(), follow_vector)

    # Normalizamos FR
    FR_vector = follow_vector/np.amax(follow_vector)

    # Metemos los resultados en la DB
    for n,user in enumerate(userlist):
        followRelationScore = FR_vector[n]
        followRelationScore = truncate(followRelationScore, 12)

        if IS_TEST:
            screen_name = client.query("select screen_name from user where id = {id}".format(id=user.oRecordData['id']))
            follow_relation_score[screen_name[0].oRecordData['screen_name']] = followRelationScore

        # if followRelationScore < 0.0000999:
        #     followRelationScore = 0.0001

        command = "update User_metrics set followRelationScore = {FR_score} where id = {id} and lastMetrics = True and topic = '{topic}'".format(id=user.oRecordData['id'], FR_score=followRelationScore, topic=topic)
        client.command(command)
    if IS_TEST:
        return follow_relation_score


# Metodo para calcular la relevancia de un usuario a partir de las otras métricas
def user_relevance_score(userlist, topic):
    print("USER RELEVANCE SCORE")
    IS_TEST = os.environ.get('IS_TEST')
    if IS_TEST:
        print ("Testing...")
        user_score = {}
    # userlist = client.query("select from User order by metrics.followers desc limit 500")
    # Pesos para el ajuste de las diferentes métricas: wr + wi + wf = 1
    wr = 0.4
    wi = 0.4
    wf = 0.2
    for user in userlist:
        # print ("Puntuación TR de user " + str(userid) + " = " + user[0].oRecordData['TR_score'])
        # print ("Puntuación UI de user " + str(userid) + " = " + user[0].oRecordData['UI_score'])
        # print ("Puntuación FR de user " + str(userid) + " = " + user[0].oRecordData['FR_score'])
        user_metrics = client.query("select from User_metrics where id = {id} and topic = '{topic}' and lastMetrics = True limit 1".format(id=user.oRecordData['id'], topic=topic))
        user_relevance = float(user_metrics[0].oRecordData['tweetRatio'])**wr + float(user_metrics[0].oRecordData['influenceUnnormalized'])**wi + float(user_metrics[0].oRecordData['followRelationScore'])**wf
        user_relevance = truncate(user_relevance, 12)
        if IS_TEST:
            screen_name = client.query("select screen_name from user where id = {id}".format(id=user.oRecordData['id']))
            user_score[screen_name[0].oRecordData['screen_name']] = user_relevance
        #print ("Relevancia de user {userid} = {user_relevance}".format(userid=user.oRecordData['id'], user_relevance=user_relevance))
        command = "update User_metrics set relevance = {user_relevance} where id = {id} and lastMetrics = True and topic = '{topic}'".format(id=user.oRecordData['id'], user_relevance=user_relevance, topic=topic)
        client.command(command)
    if IS_TEST:
        return user_score    

# # Metodo para conseguir la lista de usuarios ordenados por su relevacia
# def user_ranking():
#     ranking = client.query("select from User order by metrics.user_relevance desc limit 100")
#     for n, user in enumerate(ranking):
#         print ("En el puesto número {n} tenemos al usuario {id}".format(n=n+1,id=user.oRecordData['id']))

# # Metodo para conseguir la lista de tweets ordenados por su relevacia
# def tweet_ranking():
#     ranking = client.query("select from Tweet order by metrics.tweet_relevance desc limit 100")
#     for n, tweet in enumerate(ranking):
#         print ("En el puesto número {n} tenemos el tweet {id}".format(n=n+1,id=tweet.oRecordData['id']))


# Metodo para calcular el parametro IMPACT de un usuario
def impact_user(userlist, number_of_tweets, topic):
    print("USER IMPACT")
    IS_TEST = os.environ.get('IS_TEST')
    if IS_TEST:
        print ("Testing...")
        impact_user_score = {}
    # userlist = client.query("select from User order by metrics.followers desc limit 500")
    impact_vector = np.array([])
    # DAMPING FACTOR
    d = 0.15
    # SMOOTHING PARAMETER
    sigma = 1

    for n, user in enumerate(userlist):
        # PLANTEAR METER (in('Created_by').id) para optimizar > Cambiar ['id'] por value
        tweets_retweeted = client.query("select count(*) from (select expand(in('Retweeted_by')) from User where id = {id} limit -1) where topics containsText '{topic}' limit -1".format(id=user.oRecordData['id'], topic=topic))
        tweets_replied = client.query("select count(*) from (select expand(in('Replied_by')) from User where id = {id} limit -1) where topics containsText '{topic}' limit -1".format(id=user.oRecordData['id'], topic=topic))
        n_tweets_related = tweets_retweeted[0].oRecordData['count'] + tweets_replied[0].oRecordData['count']

        user_metrics = client.query("select from User_metrics where id = {id} and topic = '{topic}' and lastMetrics = True limit 1".format(id=user.oRecordData['id'], topic=topic))
        if not user_metrics[0].oRecordData['influenceUnnormalized']:
            user_impact = 0
        else:
            if n_tweets_related == 0:
                user_impact = float(user_metrics[0].oRecordData['influenceUnnormalized'])/number_of_tweets
            else:
                user_impact = ((float(user_metrics[0].oRecordData['influenceUnnormalized'])/(n_tweets_related+sigma))*(1-d)) + ((float(user_metrics[0].oRecordData['influenceUnnormalized'])/number_of_tweets)*d)
        user_impact = truncate(user_impact, 12)

        # if user_impact < 0.0000999:
        #     user_impact = 0 

        if IS_TEST:
            screen_name = client.query("select screen_name from user where id = {id}".format(id=user.oRecordData['id']))
            impact_user_score[screen_name[0].oRecordData['screen_name']] = user_impact
        
        command = "update User_metrics set impact = {impact} where id = {id} and lastMetrics = True and topic = '{topic}'".format(id=user.oRecordData['id'], impact=user_impact, topic=topic)
        client.command(command)
    if IS_TEST:
        return impact_user_score


# Metodo para calcular el parametro VOICE de los usuario (As-is)
def voice_user(userlist, topic):
    print("USER VOICE")
    IS_TEST = os.environ.get('IS_TEST')
    if IS_TEST:
        print ("Testing...")
        voice_user_score = {}
    #userlist = client.query("select from User order by metrics.followers desc limit 500")

    # Parametro SIGMA de suavizado
    sigma = 1
    # Calculamos VOICE para cada usuario
    for n, user in enumerate(userlist):
        tweets_user = client.query("select from (select expand(in('Created_by')) from User where id = {id} limit -1) where topics containsText '{topic}' and retweeted_status is null limit -1".format(id=user.oRecordData['id'], topic=topic))
        retweets_user = client.query("select from (select expand(in('Retweeted_by')) from User where id = {id} limit -1) where topics containsText '{topic}' limit -1".format(id=user.oRecordData['id'], topic=topic))
        
        sumatorio_tweet_TI = 0
        sumatorio_retweet_TI = 0
        for tweet in tweets_user:
            tweet_metrics = client.query("select from Tweet_metrics where id = {id} and topic = '{topic}' and lastMetrics = True limit 1".format(id=tweet.oRecordData['id'], topic=topic))
            sumatorio_tweet_TI += float(tweet_metrics[0].oRecordData['influence'])

        for retweet in retweets_user:
            retweet_metrics = client.query("select from Tweet_metrics where id = {id} and topic = '{topic}' and lastMetrics = True limit 1".format(id=retweet.oRecordData['id'], topic=topic))
            sumatorio_retweet_TI += float(retweet_metrics[0].oRecordData['influence'])

        
        retweets_user = client.query("select count(*) from (select expand(in('Retweeted_by')) from User where id = {id}) where topics containsText '{topic}'".format(id=user.oRecordData['id'], topic=topic))
        voice_t =(1/(len(tweets_user) + sigma)) * sumatorio_tweet_TI
        voice_r = (1/(retweets_user[0].oRecordData['count'] + sigma)) * sumatorio_retweet_TI

        voice_t = truncate(voice_t, 12)
        voice_r = truncate(voice_r, 12)
        #print(voice_t)
        #print(voice_r)

        if IS_TEST:
            screen_name = client.query("select screen_name from user where id = {id}".format(id=user.oRecordData['id']))
            voice_user_score[screen_name[0].oRecordData['screen_name']] = { voice_t, voice_r}

        command = "update User_metrics set voice = {voice_t}, voice_r = {voice_r} where id = {id} and lastMetrics = True and topic = '{topic}'".format(id=user.oRecordData['id'],voice_t=voice_t,voice_r=voice_r,topic=topic)
        #print(command)
        client.command(command)
        #print ("Voz usuario {n}".format(n=n+1))
    if IS_TEST:
        return voice_user_score



# Metodo para calcular el parametro TWEETRANKING de los tweets (As-is::ORIGINAL)
def tweet_relevance(number_of_tweets, topic):
    print("TWEET RELEVANCE")
    IS_TEST = os.environ.get('IS_TEST')
    if IS_TEST:
        print ("Testing...")
        tweet_relevance_score = {}
    # Parametro de ajuste ALPHA
    alpha = 0.4
    limit = 10000
    iterationRID = "#-1:-1"

    iterations = math.ceil(number_of_tweets/limit)
    print("numero de iteraciones: {iterations}".format(iterations=iterations))

    for iteration_num in range(0,iterations):
        tweetlist = client.query("select id_str from Tweet where @rid > {iterationRID} and topics containsText '{topic}' and retweeted_status is null limit {limit}".format(iterationRID=iterationRID, topic=topic, limit=limit))

        for tweet in tweetlist:
            user_creator_metrics = client.query("select expand(out('Last_metrics')) from (select expand(out('Created_by')) from Tweet where id = {id}) where topics containsText '{topic}'".format(id=tweet.oRecordData['id_str'], topic=topic))
            VR_score = 0
            if 'in_reply_to_status_id' in tweet.oRecordData:
                try:
                    VR_score = float(user_creator_metrics[0].oRecordData['voice'])
                except:
                    pass
            else:
                try:
                    VR_score = float(user_creator_metrics[0].oRecordData['voice_r'])
                except:
                    pass
            users_retweeted_metrics = client.query("select expand(out('Last_metrics')) from (select expand(out('Retweeted_by')) from Tweet where id = {id} limit -1) where topics containsText '{topic}' limit -1".format(id=tweet.oRecordData['id_str'], topic=topic))
            users_replied_metrics = client.query("select expand(out('Last_metrics')) from (select expand(out('Replied_by')) from Tweet where id = {id} limit -1) where topics containsText '{topic}' limit -1".format(id=tweet.oRecordData['id_str'], topic=topic))
            IR_score = 0
            for user_metrics in users_retweeted_metrics:
                try:
                    IR_score += float(user_metrics.oRecordData['impact'])
                except:
                    pass
            for user_metrics in users_replied_metrics:
                IR_score += float(user_metrics.oRecordData['impact'])

            tweet_relevance = alpha * VR_score + (1 - alpha) * IR_score

            if IS_TEST:
                tweet_relevance_score[tweet.oRecordData['id_str']] = tweet_relevance
            
            command = "update Tweet_metrics set relevance = {tweet_relevance} where id = {id} and topic = '{topic}'".format(id=tweet.oRecordData['id_str'],tweet_relevance=tweet_relevance, topic = topic)
            client.command(command)

        iterationRID = tweet._rid
        if IS_TEST:
            return tweet_relevance_score
        print ("Tweet iterationRID".format(iterationRID=iterationRID))

def user_metrics_object_creation(user, tweet_ratio, topic):
    user_id = user.oRecordData['id']

    ts = time.time()
    date_ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    lastMetrics = client.query("select from User_metrics where id = {id} and lastMetrics = True".format(id=user_id))
    if lastMetrics:
        client.command("update User_metrics set lastMetrics = False where lastMetrics = True and id = {id} and topic = '{topic}'".format(id=user_id, topic = topic))
        client.command("delete edge Last_metrics from (select from User where id = {id})".format(id=user_id))
    if 'followers_count' in user.oRecordData:
        client.command("insert into User_metrics set id = {id}, lastMetrics = True, followers = {followers}, following = {following}, date = '{date}', timestamp = {timestamp}, tweetRatio = {tweet_ratio}, statuses_count = {statuses_count}, topic = '{topic}', influence = 0, influenceUnnormalized = 0, voice = 0, voice_r = 0, impact = 0, relevance = 0, complete = True".format(id=user_id,followers=user.oRecordData['followers_count'],following=user.oRecordData['friends_count'], date=date_ts, timestamp = ts, tweet_ratio = tweet_ratio, statuses_count = user.oRecordData['statuses_count'], topic = topic))    
        client.command("create edge Last_metrics from (select from User where id = {id_metrics}) to (select from User_metrics where id = {id} and lastMetrics = True)".format(id=user_id, id_metrics=user_id))
    else:
        pass

def tweet_metrics_object_creation(tweet, topic):
    tweet_id = tweet.oRecordData['id']

    ts = time.time()
    date_ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    lastMetrics = client.query("select from Tweet_metrics where id = {id} and lastMetrics = True".format(id=tweet_id))
    if lastMetrics:
        client.command("update Tweet_metrics set lastMetrics = False where lastMetrics = True and id = {id} and topic = '{topic}'".format(id=tweet_id, topic=topic))
        client.command("delete edge Last_metrics from (select from Tweet where id = {id})".format(id=tweet_id))
    client.command("insert into Tweet_metrics set id = {id}, topic= '{topic}', lastMetrics = True, influence = 0, relevance = 0, complete = True, date = '{date}', timestamp = {timestamp}".format(id=tweet_id, topic=topic, date=date_ts, timestamp=ts))
    client.command("create edge Last_metrics from (select from Tweet where id = {id}) to (select from Tweet_metrics where id = {id} and lastMetrics = True)".format(id=tweet_id))


# METODO PARA REALIZAR LA FASE DE PREPARACION
def preparation_phase(topic):
    print("PREPARATION PHASE")
    skip = 0
    # Cargamos los usuarios que han generado algún tweet
    userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText '{topic}' and depth < 2 limit -1".format(topic=topic))
    #print(userlist)
    # Calculamos el numero de usuarios y tweets que tenemos en la DB
    number_of_tweets = client.query("select count(*) as count from Tweet where topics containsText '{topic}' and retweeted_status is null".format(topic=topic))
    number_of_tweets = number_of_tweets[0].oRecordData['count']
    number_of_users = len(userlist);

    print("Numero de Tweet originales: {tweets}".format(tweets=number_of_tweets))
    print("Numero de usuarios con tweets: {usuarios}".format(usuarios=number_of_users))


    # CREA OBJETOS DE METRICAS DE USUARIO
    user_tweetratio_score(userlist, topic)
    influence_score(userlist, number_of_users, number_of_tweets, topic)
    follow_relation_factor_user(userlist, number_of_users, topic)
    impact_user(userlist, number_of_tweets, topic)
    voice_user(userlist, topic)
    #user_relevance_score(userlist, topic)
    tweet_relevance(number_of_tweets,topic)
    client.command("update Topic set tweet_count = {tweets}, user_count = {users} where name = '{topic}'".format(tweets=number_of_tweets, users=number_of_users, topic=topic))

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])    

def main_phase(tweet, topic):
    print("MAIN PHASE")
    
    #Parámetros predefinidos
    p = -3.0
    alpha = 0.4

    #Comprobamos si hay métricas existentes para ese topic
    metricsInDB = client.query("select from tweet_metrics where topic = '{topic}'".format(topic = topic))
    if not metricsInDB:
        return "You need to run preparation_phase for the topic {topic}".format(topic=topic)


    # Comprobamos si el tweet es un reply
    if 'in_reply_to_status_id' in tweet:
        if tweet['in_reply_to_status_id'] != None:
            original_tweet = client.query("select from tweet where id_str = {id_str}".format(id_str = tweet['in_reply_to_status_id_str']))

    # Comprobamos si el tweet es un retweet
    if 'retweeted_status' in tweet:
        if tweet['retweeted_status'] != None:
            original_user = client.query("select from user where id = {id}".format(id=tweet['user']['id']))
    
    # Comprobamos si tiene user definido en nuestra base de datos
    user = client.query("select from user where id = {id}".format(id=tweet['user']['id']))
    if not user:
        return "User is not defined"

    # Actualizamos las voces que son 0 siguiendo la formula de Noro de ponerle la minima voz multiplicada por un factor 'p'

    voice_min = client.query("select min(voice) from user_metrics where topic containsText '{topic}'".format(topic=topic))
    voice_r_min = client.query("select min(voice_r) from user_metrics where topic containsText '{topic}'".format(topic=topic))
    user_metrics = client.query("select expand(out('Last_metrics')) from (select expand(out('Created_by')) from Tweet where id_str = {id}) where topics containsText '{topic}'".format(id=tweet['id_str'], topic=topic))
    if user_metrics[0].oRecordData['voice'] == 0:
          new_voice = float(voice_min[0].oRecordData['min']*p)
          client.command("update user_metrics set voice = {voice} where id = {id}".format(id=user[0].oRecordData['id'],voice=new_voice))
    if user_metrics[0].oRecordData['voice_r'] == 0:
          new_voice_r = float(voice_r_min[0].oRecordData['min']*p)
          client.command("update user_metrics set voice = {voice} where id = {id}".format(id=user[0].oRecordData['id'],voice=new_voice_r))


    # Tweet relevance calculated for the tweet

    VR_score = 0
    if 'retweeted_status' in tweet:        
        user_original_metrics = client.query("select expand(out('Last_metrics')) from (select expand(out('Created_by')) from Tweet where id_str = {id}) where topics containsText '{topic}'".format(id=tweet['retweeted_status']['id_str'], topic=topic))
        VR_score = float(user_original_metrics[0].oRecordData['voice'])
    else:
        VR_score = float(user_metrics[0].oRecordData['voice'])

    IR_score = 0
    users_retweeted_metrics = client.query("select expand(out('Last_metrics')) from (select expand(out('Retweeted_by')) from Tweet where id_str = {id}) where topics containsText '{topic}'".format(id=tweet['id_str'], topic=topic))
    users_replied_metrics = client.query("select expand(out('Last_metrics')) from (select expand(out('Replied_by')) from Tweet where id_str = {id}) where topics containsText '{topic}'".format(id=tweet['id_str'], topic=topic))
    
    for user_metrics in users_retweeted_metrics:
        IR_score += float(user_metrics[0].oRecordData['impact'])
    for user_metrics in users_replied_metrics:
        IR_score += float(user_metrics[0].oRecordData['impact'])

    tweet_relevance = alpha * VR_score + (1 - alpha) * IR_score

    
    command = "update Tweet_metrics set relevance = {tweet_relevance} where id = {id} and topic = '{topic}'".format(id=tweet['id_str'],tweet_relevance=tweet_relevance, topic = topic)
    client.command(command)

    return("Tweet relevance is {relevance}".format(relevance=tweet_relevance))
#EJECUCION
def execution():
    topics = client.query("select from Topic limit -1")
    for topicObject in topics:
        topic = topicObject.oRecordData['name']
        if topic != "default":        
            print(topic)
            preparation_phase(topic)

    print("::::::::FIN::::::::")

if __name__ == '__main__':

    client = pyorient.OrientDB("localhost", 2424)
    session_id = client.connect("root", "root")
    client.db_open("mixedemotions", "admin", "admin")

    preparation_phase()

    #user_ranking()
    #tweet_ranking()

    print("::::::::FIN::::::::")