import unittest
import pyorient
import json
import random
import csv

import scaner.tasks as task
import scaner.influence_metrics as metrics


class UnitTests(unittest.TestCase):

    client = pyorient.OrientDB("orientdb_test", 2424)
    session_id = client.connect("root", "root")
    client.db_open("mixedemotions", "admin", "admin")
    userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'Euthanasia' and depth < 2 limit -1")
    number_of_tweets = client.query("select count(*) as count from Tweet where topics containsText 'Euthanasia'")
    number_of_tweets = number_of_tweets[0].oRecordData['count']
    number_of_users = len(userlist);

    def test_user_metrics(self):
        js = task.get_user_metrics(998261900)
        #print (js)
        assert  all (k in js for k in ('influenceUnnormalized','influence','voice_r','tweetRatio','lastMetrics','relevance','statuses_count','complete','following','impact','id','voice','date','followers'))

    def test_user_in_DB(self):
    	js = task.user(998261900)
    	assert 'id' in js

    def test_user_not_in_DB(self):
        js = task.user(random.randint(0, 20))
        assert js == "User not found in DB"

    def test_user_network(self):
        js = task.user_network(998261900)
        print(len(js))
        network = 2
        assert len(js) == network

    def test_tweet_in_DB(self):
        js = task.tweet(545870569300688896)
        assert 'id' in js

    def test_tweet_not_in_DB(self):
        js = task.tweet(random.randint(0, 20))
        assert js == "Tweet not found in DB"

    def test_tweet_metrics(self):
        js = task.get_tweet_metrics(545870569300688896)
        assert  all (k in js for k in ('date','influence','lastMetrics','relevance','complete','id','topic','timestamp'))

    def test_tweet_history(self):
        js = task.tweet_history(545870569300688896)
        #print (js)
        for i in js:
            if not all (k in i for k in ('date','influence','lastMetrics','relevance','complete','id','topic','timestamp')):
                assert False
        assert True

    def test_auser_tweetratio_score(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'Euthanasia' and depth < 2 limit -1")
        js = metrics.user_tweetratio_score(userlist,'Euthanasia')
        #print (js)
        json = {}
        with open('tests/results/bigdata/bigdata.tr.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                json[row[0]] = row[1]
            #print(json)
        client.db_close()
        assert js == json
    
    def test_binfluence_score(self):   
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'Euthanasia' and depth < 2 limit -1")
        number_of_tweets = client.query("select count(*) as count from Tweet where topics containsText 'Euthanasia'")
        number_of_tweets = number_of_tweets[0].oRecordData['count']
        number_of_users = len(userlist);
        js = metrics.influence_score(userlist, number_of_users, number_of_tweets, 'Euthanasia')
        #print (js)
        client.db_close()
        json = {}
        with open('tests/results/bigdata/test.is.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                json[row[0]] = row[1]
                assert json[row[0]] == js[row[0]]
            #print(json)
              

    def test_cfollow_relation_factor_user(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'Euthanasia' and depth < 2 limit -1")
        number_of_users = len(userlist);
        js = metrics.follow_relation_factor_user(userlist, number_of_users, 'Euthanasia')
        #print(js)
        json = {}
        with open('tests/results/bigdata/bigdata.fr.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                json[row[0]] = row[1]        
        client.db_close()
        assert js == json

    def test_dimpact_user(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'Euthanasia' and depth < 2 limit -1")
        number_of_tweets = client.query("select count(*) as count from Tweet where topics containsText 'Euthanasia'")
        number_of_tweets = number_of_tweets[0].oRecordData['count']
        js = metrics.impact_user(userlist, number_of_tweets, 'Euthanasia')
        #print(js)
        json = {}
        with open('tests/results/bigdata/bigdata.ui.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                json[row[0]] = row[1]
        client.db_close()
        assert js == json

    def test_evoice_user(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'Euthanasia' and depth < 2 limit -1")
        js = metrics.voice_user(userlist, 'Euthanasia')
        #print (js)
        json = {}
        with open('tests/results/bigdata/bigdata.voice_impact.asis.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                #print (row)
                json[row[0]] = {'voice_retweet': row[2], 'voice_tweet': row[1]}         
        client.db_close()
        #print(json)
        assert js == json

    def test_ftweet_relevance(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        number_of_tweets = client.query("select count(*) as count from Tweet where topics containsText 'Euthanasia'")
        number_of_tweets = number_of_tweets[0].oRecordData['count']
        js = metrics.tweet_relevance(number_of_tweets, 'Euthanasia')
        client.db_close()
        #print (js)
        json = {}
        with open('tests/results/bigdata/test.tr.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                json[row[0]] = row[1]
        assert js == json

    def test_guser_relevance(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'Euthanasia' and depth < 2 limit -1")
        js = metrics.user_relevance_score(userlist, 'Euthanasia')
        #print (js)
        json = {}
        with open('tests/results/bigdata/bigdata.userrel.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                json[row[0]] = row[1]         
        client.db_close()
        assert js == json