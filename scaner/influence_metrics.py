import pyorient
import math
import numpy as np
import time
import datetime
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix
import gc

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "root")
client.db_open("mixedemotions", "admin", "admin")

# FALTA TENER EL NÚMERO TOTAL DE TWEETS DE UN USUARIO FUERA DE LA BUSQUEDA
# Metodo para calcular la metrica TR SCORE de todos los usuarios
def user_tweetratio_score(userlist):
    print("USER TWEETRATIO")
    # userlist = client.query("select from User limit -1")
    for user in userlist:
        user_metrics_list = client.query("select from User_metrics where id = {id} order by date desc".format(id = user.oRecordData['id']))
        tweets_from_user_in_DB = client.query("select count(in('Created_by')) from User where id = {id}".format(id = user.oRecordData['id']))

        if len(user_metrics_list) > 1:
            tweet_difference = user_metrics_list[0].oRecordData['statuses_count'] - user_metrics_list[-1].oRecordData['statuses_count']
            if tweet_difference == 0:
                tweet_ratio = tweets_from_user_in_DB[0].oRecordData['count'] / user_metrics_list[0].oRecordData['statuses_count']
            else:
                tweet_ratio = tweets_from_user_in_DB[0].oRecordData['count'] / tweet_difference
        else:
            tweet_ratio = tweets_from_user_in_DB[0].oRecordData['count'] / user_metrics_list[0].oRecordData['statuses_count']

        # CREAMOS EL OBJETO DE METRICAS DE USUARIO
        user_metrics_object_creation(user, tweet_ratio)

        # tweets_related_user = client.query("select from Tweet where user_id = '{userid}'".format(userid=user.oRecorData['id']) )
        # tweets_related_user = len(tweets_related_user)
        # tweets_total_user = int(user.oRecordData['total_tweets'])
        # TR_score = tweets_related_user/tweets_total_user
        # command = "update (select from User where id = {id}) set metrics.TR_score = {TR_score}".format(id=user.oRecordData['id'], TR_score=TR_score)
        # #command = "update (select from User where id = '" + str(user.oRecordData['userid']) + "') set TR_score = '" + str(0.5) + "'"
        # client.command(command)


# Metodo para calcular la metrica UI SCORE
def influence_score(userlist, number_of_users, number_of_tweets):
    print("INFLUENCE SCORE")
    # Parametros
    limit = 10000
    iterationRID = "#-1:-1"
    index = 0
    # iterations = max([(number_of_users/limit), (number_of_tweets/limit)])
    iterations = math.ceil(number_of_tweets/limit)
    print("numero de iteraciones: {iterations}".format(iterations=iterations))

    # Creamos las matrices At, Ar y As vacia
    At = lil_matrix((number_of_tweets,number_of_users))
    Ar = lil_matrix((number_of_users,number_of_tweets))
    As = lil_matrix((number_of_users,number_of_tweets))

    # userlist = client.query("select from User order by metrics.followers desc limit 500")
    # userlist = client.query("select from User limit -1")

    for iteration_num in range(0,iterations):
        tweetlist = client.query("select id from Tweet where @rid > {iterationRID} limit {limit}".format(iterationRID=iterationRID, limit=limit))

        # Iteramos los usuarios y los tweets para rellenar las matrices
        index_start = index
        for n,user in enumerate(userlist):

            # Creamos el vector para la matriz At
            user_tweet_At = np.array([])
            # Creamos el vector para la matriz Ar
            tweet_user_Ar = np.array([])
            # Creamos el vector para la matriz As (FALTA PARAMETRO s)
            user_user_As = np.array([])

            print("HAGO LAS QUERYS PARA LAS MATRICES")
            # PUEDO OPTIMIZAR METIENDO ESTAS QUERYS EN LOS IF DE DEBAJO
            # PLANTEAR METER (in('Created_by').id) para optimizar > Cambiar ['id'] por value

            user_created = client.query("select expand(in('Created_by')) from User where id ={user_id}".format(user_id=user.oRecordData['id']))
            
            user_retweeted = client.query("select expand(in('Retweeted_by')) from  User where id ={user_id}".format(user_id=user.oRecordData['id']))

            user_replied = client.query("select expand(in('Replied_by')) User where id ={user_id}".format(user_id=user.oRecordData['id']))

            user_follows_created = client.query("select expand(out('Follows').in('Created_by')) from User where id ={user_id}".format(user_id=user.oRecordData['id']))

            user_follows_retweeted = client.query("select expand(out('Follows').in('Retweeted_by')) from User where id ={user_id}".format(user_id=user.oRecordData['id']))

            print("COMIENZO A CALCULAR")
            for tweet in tweetlist:
                found_At = False
                found_Ar = False
                found_As = False

                # Calculamos el vector para At y para Ar
                for retweeted in user_retweeted:
                    if retweeted.oRecordData['id'] == tweet.oRecordData['id']:
                        user_tweet_At = np.append(user_tweet_At, np.ones(1))
                        found_At = True
                        tweet_user_Ar = np.append(tweet_user_Ar, np.ones(1))
                        found_Ar = True
                        break

                if not found_At:        
                    for created in user_created:
                        if created.oRecordData['id'] == tweet.oRecordData['id']:
                            user_tweet_At = np.append(user_tweet_At, np.ones(1))
                            found_At = True
                            break

                if not found_Ar:
                    for replied in user_replied:
                        if replied.oRecordData['tid'] == tweet.oRecordData['tid']:
                            tweet_user_Ar = np.append(tweet_user_Ar, np.ones(1))
                            found_Ar = True
                            break 

                # Calculamos el vector para As
                for tweet_follow in user_follows_created:
                    if tweet_follow.oRecordData['id'] == tweet.oRecordData['id']:
                        user_user_As = np.append(user_user_As, np.ones(1))
                        found_As = True
                        break
                if not found_As:
                    for retweet_follow in user_follows_retweeted:
                        if tweet_follow.oRecordData['id'] == tweet.oRecordData['id']:
                            user_user_As = np.append(user_user_As, np.ones(1))
                            found_As = True
                            break

                if not found_As:
                    user_user_As = np.append(user_user_As,np.zeros(1))
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
    d = 0.5

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

    for k in range(1, 10):
        tweets_vector = Ba_transpose.dot(users_vector)
        users_vector = Bt_transpose.dot(tweets_vector)

    # LIMPIAMOS MEMORIA
    Ba_transpose = 0
    Bt_transpose = 0
    gc.collect()

    # Normalizamos UI
    try:
        UI_vector = users_vector/np.amax(users_vector)
    except:
        print("USUARIOS NO RELACIONADOS")

    #ALMACENAMOS EN LA DB LAS PUNTUACIONES
    for n,user in enumerate(userlist):
        
        UI = UI_vector[n]
        UI_unnormalized = users_vector[n]
        if UI_unnormalized < 0.0000999:
            UI_unnormalized = 0
        if UI < 0.0000999:
            UI = 0
        command = "update User_metrics set influence={UI_score}, influenceUnnormalized={UI_unnormalized} where id={user_id} and lastMetrics = True".format(user_id=user.oRecordData['id'], UI_score=UI, UI_unnormalized=UI_unnormalized)
        print (command)
        client.command(command)

    newindex = 0
    iterationRID = "#-1:-1"
    for iteration_num in range(0,iterations):
        tweetlist = client.query("select id from Tweet where @rid > {iterationRID} limit {limit}".format(iterationRID=iterationRID, limit=limit))

        for n,tweet in enumerate(tweetlist):

            # CREAMOS EL OBJETO DE METRICAS TWEET Y LO RELLENAMOS
            tweet_metrics_object_creation(tweet)

            command = "update Tweet_metrics set influence = {TI_score} where id = {id} and Last_metrics = True".format(id=tweet.oRecordData['id'], TI_score=tweets_vector[n+newindex])
            client.command(command)
        newindex += 10000 
        iterationRID = tweet._rid

    # while (error_u > 0.1) or (error_t > 0.1):
    #     error_u = -np.mod(users_vector)
    #     error_t = -np.mod(tweets_vector)
    #     tweets_vector = np.dot(Ba.transpose(), users_vector)
    #     users_vector = np.dot(Bt.transpose(), tweets_vector)
    #     error_u += np.mod(users_vector)
    #     error_t += np.mod(tweets_vector)

    
def follow_relation_factor_user(userlist, number_of_users):
    print("FOLLOW RELATION FACTOR USER")
    # userlist = client.query("select from User order by metrics.followers desc limit 500")
    # userlist = client.query("select from User limit -1")

    Af = np.zeros((number_of_users, number_of_users))

    for n, user in enumerate(userlist):
        user_user_Af = np.array([])

        # PLANTEAR METER (in('Created_by').id) para optimizar > Cambiar ['id'] por value

        user_follows = client.query("select expand(out('Follows')) from User where id = {id}".format(id=user.oRecordData['id']))
        
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
    d = 0.5

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
    
    for k in range(1, 500):
        follow_vector = np.dot(Bf.transpose(), follow_vector)

    # Normalizamos FR
    FR_vector = follow_vector/np.amax(follow_vector)

    # Metemos los resultados en la DB
    for n,user in enumerate(userlist):
        command = "update User_metrics set followRelationScore = {FR_score} where id = {id} and lastMetrics = True".format(id=user.oRecordData['id'], FR_score=FR_vector[n])
        client.command(command)


# Metodo para calcular la relevancia de un usuario a partir de las otras métricas
def user_relevance_score(userlist):
    print("USER RELEVANCE SCORE")
    # userlist = client.query("select from User order by metrics.followers desc limit 500")
    # Pesos para el ajuste de las diferentes métricas: wr + wi + wf = 1
    wr = 0.1
    wi = 0.5
    wf = 0.4
    for user in userlist:
        # print ("Puntuación TR de user " + str(userid) + " = " + user[0].oRecordData['TR_score'])
        # print ("Puntuación UI de user " + str(userid) + " = " + user[0].oRecordData['UI_score'])
        # print ("Puntuación FR de user " + str(userid) + " = " + user[0].oRecordData['FR_score'])
        user_metrics = client.query("select expand(out('Last_metrics')) from User where id = {id}".format(id=user.oRecordData['id']))
        user_relevance = float(user_metrics[0].oRecordData['tweetRatio'])**wr + float(user_metrics[0].oRecordData['influence'])**wi + float(user_metrics[0].oRecordData['followRelationScore'])**wf
        print ("Relevancia de user {userid} = {user_relevance}".format(userid=user.oRecordData['id'], user_relevance=user_relevance))
        command = "update User_metrics set relevance = {user_relevance} where id = {id} and lastMetrics = True".format(id=user.oRecordData['id'], user_relevance=user_relevance)
        client.command(command)

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
def impact_user(userlist, number_of_tweets):
    print("USER IMPACT")
    # userlist = client.query("select from User order by metrics.followers desc limit 500")
    impact_vector = np.array([])
    # DAMPING FACTOR
    d = 0.5
    # SMOOTHING PARAMETER
    sigma = 0.5

    for n, user in enumerate(userlist):
        # PLANTEAR METER (in('Created_by').id) para optimizar > Cambiar ['id'] por value
        tweets_retweeted = client.query("select count(in('Retweeted_by')) from User where id = {id}".format(id=user.oRecordData['id']))
        tweets_replied = client.query("select count(in('Replied_by')) from User where id = {id}".format(id=user.oRecordData['id']))
        n_tweets_related = tweets_retweeted[0].oRecordData['count'] + tweets_replied[0].oRecordData['count']

        user_metrics = client.query("select expand(out('Last_metrics')) from User where id = {id}".format(id=user.oRecordData['id']))
        if not user_metrics[0].oRecordData['influenceUnnormalized']:
            user_impact = 0
        else:
            if n_tweets_related == 0:
                user_impact = float(user_metrics[0].oRecordData['influenceUnnormalized'])/number_of_tweets
            else:
                user_impact = ((float(user_metrics[0].oRecordData['influenceUnnormalized'])/(n_tweets_related+sigma))*(1-d)) + ((float(user_metrics[0].oRecordData['influenceUnnormalized'])/number_of_tweets)*d)
        if user_impact < 0.0000999:
            user_impact = 0   
        command = "update User_metrics set impact = {impact} where id = {id} and lastMetrics = True".format(id=user.oRecordData['id'], impact=user_impact)
        client.command(command)


# Metodo para calcular el parametro VOICE de los usuario (As-is)
def voice_user(userlist):
    print("USER VOICE")
    #userlist = client.query("select from User order by metrics.followers desc limit 500")

    # Parametro SIGMA de suavizado
    sigma = 0.5
    # Calculamos VOICE para cada usuario
    for n, user in enumerate(userlist):
        tweets_user = client.query("select expand(in('Created_by')) from User where id = {id}".format(id=user.oRecordData['id']))
        retweets_user = client.query("select expand(in('Retweeted_by')) from User where id = {id}".format(id=user.oRecordData['id']))
        sumatorio_tweet_TI = 0
        sumatorio_retweet_TI = 0
        for tweet in tweets_user:

            tweet_metrics = client.query("select expand(out('Last_metrics')) from Tweet where id = {id}".format(id=tweet.oRecordData['id']))

            try:
                sumatorio_tweet_TI += float(tweet_metrics.oRecordData['influence'])
            except:
                pass
        for retweet in retweets_user:

            retweet_metrics = client.query("select expand(out('Last_metrics')) from Tweet where id = {id}".format(id=tweet.oRecordData['id']))

            try:
                sumatorio_retweet_TI += float(retweet_metrics.oRecordData['influence'])
            except:
                pass

        retweets_user = client.query("select count(in('Retweeted_by')) from User where id = {id}".format(id=user.oRecordData['id']))
        voice_t = (1/(len(tweets_user) + sigma)) * sumatorio_tweet_TI
        voice_r = (1/(retweets_user[0].oRecordData['count'] + sigma)) * sumatorio_retweet_TI

        command = "update User_metrics set voice = {voice_t}, voice_r = {voice_r} where id = {id} and lastMetrics = True".format(id=user.oRecordData['id'],voice_t=voice_t,voice_r=voice_r)
        client.command(command)
        print ("Voz usuario {n}".format(n=n+1))


# Metodo para calcular el parametro TWEETRANKING de los tweets (As-is::ORIGINAL)
def tweet_relevance(number_of_tweets):
    print("TWEET RELEVANCE")
    # Parametro de ajuste ALPHA
    alpha = 0.5
    limit = 10000
    iterationRID = "#-1:-1"

    iterations = math.ceil(number_of_tweets/limit)
    print("numero de iteraciones: {iterations}".format(iterations=iterations))

    for iteration_num in range(0,iterations):
        tweetlist = client.query("select id from Tweet where @rid > {iterationRID} limit {limit}".format(iterationRID=iterationRID, limit=limit))

        for tweet in tweetlist:
            user_creator_metrics = client.query("select expand(out('Created_by').out('Last_metrics')) from Tweet where id = {id}".format(id=tweet.oRecordData['id']))
            VR_score = 0
            if 'in_reply_to_status_id' in tweet.oRecordData:
                try:
                    VR_score = float(user_creator_metrics[0].oRecordData['voice_t'])
                except:
                    pass
            else:
                try:
                    VR_score = float(user_creator_metrics[0].oRecordData['voice_r'])
                except:
                    pass
            users_retweeted_metrics = client.query("select expand(out('Retweeted_by').out('Last_metrics')) from Tweet where id = {id}".format(id=tweet.oRecordData['id']))
            users_replied = client.query("select expand(out('Replied_by').out('Last_metrics')) from Tweet where id = {id}".format(id = tweet.oRecordData['id']))
            IR_score = 0
            for user_metrics in users_retweeted_metrics:
                try:
                    IR_score += float(user_metrics.oRecordData['impact'])
                except:
                    pass
            for user in users_replied:
                IR_score += float(user_metrics.oRecordData['impact'])

            tweet_relevance = alpha * VR_score + (1 - alpha) * IR_score

            command = "update Tweet_metrics set relevance = {tweet_relevance} where id = {id}".format(id=tweet.oRecordData['id'],tweet_relevance=tweet_relevance)
            client.command(command)

        iterationRID = tweet._rid
        print ("Tweet iterationRID".format(iterationRID=iterationRID))

def user_metrics_object_creation(user, tweet_ratio):
    user_id = user.oRecordData['id']

    ts = time.time()
    date_ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    lastMetrics = client.query("select from User_metrics where id = {id} and lastMetrics = True".format(id=user_id))
    if lastMetrics:
        client.command("update User_metrics set lastMetrics = False where lastMetrics = True and id = {id}".format(id=user_id))
        client.command("delete edge Last_metrics from (select from User where id = {id})".format(id=user_id))
    if 'followers_count' in user.oRecordData:
        client.command("insert into User_metrics set id = {id}, lastMetrics = True, followers = {followers}, following = {following}, date = '{date}', tweetRatio = {tweet_ratio}, influence = 0, influenceUnnormalized = 0, voice = 0, voice_r = 0, impact = 0, relevance = 0, complete = True".format(id=user_id,followers=user.oRecordData['followers_count'],following=user.oRecordData['friends_count'], date=date_ts, tweet_ratio = tweet_ratio))    
        client.command("create edge Last_metrics from (select from User where id = {id_metrics}) to (select from User_metrics where id = {id} and lastMetrics = True)".format(id=user_id, id_metrics =user_id))
        print("METRICAS CREADAS")
    else:
        pass

def tweet_metrics_object_creation(tweet):
    tweet_id = tweet.oRecordData['id']

    ts = time.time()
    date_ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    lastMetrics = client.query("select from Tweet_metrics where id = {id} and lastMetrics = True".format(id=tweet_id))
    if lastMetrics:
        client.command("update Tweet_metrics set lastMetrics = False where lastMetrics = True and id = {id}".format(id=tweet_id))
        client.command("delete edge Last_metrics from (select from Tweet where id = {id})".format(id=tweet_id))
    client.command("insert into Tweet_metrics set id = {id}, lastMetrics = True, influence = 0, relevance = 0, complete = True, date = '{date}'".format(id=tweet_id, date=date_ts))
    client.command("create edge Last_metrics from (select from Tweet where id = {id}) to (select from Tweet_metrics where id = {id} and lastMetrics = True)".format(id=tweet_id))


# METODO PARA REALIZAR LA FASE DE PREPARACION
def preparation_phase():
    print("PREPARATION PHASE")
    # Cargamos los usuarios
    userlist = client.query("select id, followers_count, friends_count from User where pending = false limit -1")
    # Calculamos el numero de usuarios y tweets que tenemos en la DB
    number_of_tweets = client.query("select count(*) as count from Tweet")
    number_of_tweets = number_of_tweets[0].oRecordData['count']
    number_of_users = client.query("select count(*) as count from User where pending = false")
    number_of_users = number_of_users[0].oRecordData['count']

    print("Numero de Tweet: {tweets}".format(tweets=number_of_tweets))
    print("Numero de usuarios: {usuarios}".format(usuarios=number_of_users))

    # CREA OBJETOS DE METRICAS DE USUARIO
    user_tweetratio_score(userlist)

    influence_score(userlist, number_of_users, number_of_tweets)
    follow_relation_factor_user(userlist, number_of_users)
    impact_user(userlist, number_of_tweets)
    voice_user(userlist)
    tweet_relevance(number_of_tweets)
    user_relevance_score(userlist)
        


#EJECUCION
def execution():
    preparation_phase()

    print("::::::::FIN::::::::")

if __name__ == '__main__':

    client = pyorient.OrientDB("localhost", 2424)
    session_id = client.connect("root", "root")
    client.db_open("mixedemotions", "admin", "admin")

    preparation_phase()

    #user_ranking()
    #tweet_ranking()

    print("::::::::FIN::::::::")
