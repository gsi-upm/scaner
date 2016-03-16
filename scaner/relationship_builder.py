import pyorient

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "root")
client.db_open("mixedemotions", "admin", "admin")

def users_relationships_creation():
    pass

def tweets_relationships_creation():
    limit = 10000
    iterationRID = "#-1:-1"

    iterations = math.ceil(number_of_tweets/limit)
    print("numero de iteraciones: {iterations}".format(iterations=iterations)

    for iteration_num in range(0,iterations):
        tweetlist = client.query("select from Tweet where @rid > {iterationRID} limit {limit}".format(iterationRID=iterationRID, limit=limit))

        for tweet in tweetlist:
            tweet_id=tweet.oRecordData['id']
            # Primero relacionamos el tweet con su creador
            user_id = tweet.oRecordData['user_id']
            user = client.query("select from User where id = {user_id}".format(user_id=user_id))
            # En caso de no tener el usuario, lo descargamos
            if not user:

                #LLAMAR AL METODO PARA PEDIR EL USUARIO
                pass

            # Creamos la relacion de Created_by
            command = "create edge Created_by from (select from Tweet where id = {tweet_id}) to (select from User where user_id = {user_id})".format(tweet_id=tweet_id,user_id=user_id)
            client.command(command)

            # Ahora relacionamos el tweet con un posible con el tweet original en caso de ser un retweet
            original_id=tweet.oRecordData['retweeted_status']['id']
            if original_id:
                # Comprobamos si tenemos el original
                original_tweet = client.query("select from Tweet where id = {tweet_id}".format(tweet_id=original_id))
                # En caso de no tener el twee, lo descargamos
                if not original_tweet:

                    #LLAMAR AL METODO PARA PEDIR TWEET
                    pass

                # Creamos la relacion de Retweet
                command = "create edge Retweet from (select from Tweet where id = {tweet_id}) to (select from Tweet where id = {original_id})".format(tweet_id=tweet_id,original_id=original_id)
                client.command(command)

                # Creamos la relación Retweeted_by
                original_user_id = tweet.oRecordData['retweeted_status']['user_id']
                original_user = client.query("select from User where id = {user_id}".format(user_id=original_user_id))
                # En caso de no tener el usuario, lo descargamos
                if not original_user:

                    #LLAMAR AL METODO PARA PEDIR EL USUARIO
                    pass

                # Creamos la relacion de Retweeted_by
                command = "create edge Retweeted_by from (select from Tweet where id = {tweet_id}) to (select from User where id = {user_id})".format(tweet_id=original_id,user_id=user_id)
                client.command(command)

        # Aumentamos el RID para cargar los siguientes tweets
        iterationRID = tweet._rid



def individual_user_relationships_creation(user_id):
    client.command("create edge Created_by from (select from Tweet where user_id={user_id} to (select from User where id={user_id})".format(user_id=user_id))
    client.command("create edge Retweeted_by from (select expand(out('Retweet')) from (select from Tweet where user_id={user_id})) to (select from User where id={user_id})".format(user_id=user_id))
    #TODO RELACION FOLLOW

def individual_tweet_relationships_creation():
    pass