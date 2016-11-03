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
    userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'nuclear' and depth < 2 limit -1")
    number_of_tweets = client.query("select count(*) as count from Tweet where topics containsText 'nuclear'")
    number_of_tweets = number_of_tweets[0].oRecordData['count']
    number_of_users = len(userlist);

    def test_user_metrics(self):
        js = task.get_user_metrics(85727936)
        #print (js)
        assert  all (k in js for k in ('influenceUnnormalized','influence','voice_r','tweetRatio','lastMetrics','relevance','statuses_count','complete','following','impact','id','voice','date','followers'))

    def test_user_in_DB(self):
    	js = task.user(85727936)
    	assert 'id' in js

    def test_user_not_in_DB(self):
        js = task.user(random.randint(0, 20))
        assert js == "User not found in DB"

    def test_user_network(self):
        js = task.user_network(85727936)
        print(len(js))
        network = 12628
        assert len(js) == network

    def test_tweet_in_DB(self):
        js = task.tweet(546587081934258176)
        assert 'id' in js

    def test_tweet_not_in_DB(self):
        js = task.tweet(random.randint(0, 20))
        assert js == "Tweet not found in DB"

    def test_tweet_metrics(self):
        js = task.get_tweet_metrics(546587081934258176)
        assert  all (k in js for k in ('date','influence','lastMetrics','relevance','complete','id','topic','timestamp'))

    def test_tweet_history(self):
        js = task.tweet_history(546587081934258176)
        #print (js)
        for i in js:
            if not all (k in i for k in ('date','influence','lastMetrics','relevance','complete','id','topic','timestamp')):
                assert False
        assert True

    def test_user_tweetratio_score(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'nuclear' and depth < 2 limit -1")
        js = metrics.user_tweetratio_score(userlist,'nuclear')
        print (js)
        json = {}
        with open('tests/results/bigdata/bigdata.tr.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                json[row[0]] = row[1]
            #print(json)
        client.db_close()
        assert js == json
    
    def test_influence_score(self):   
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'nuclear' and depth < 2 limit -1")
        number_of_tweets = client.query("select count(*) as count from Tweet where topics containsText 'nuclear'")
        number_of_tweets = number_of_tweets[0].oRecordData['count']
        number_of_users = len(userlist);
        js = metrics.influence_score(userlist, number_of_users, number_of_tweets, 'nuclear')
        print (js)
        influence_calculated = {85727936: '0.000000000000', 15978752: '0.000024812343', 546861511633682433: '0.274291885177', 356195126: '0.000000000000', 546796939535065088: '1.000000000000', 546860197587591168: '0.000000000000', 546861939037446144: '0.274291885177', 546857890833641472: '0.000000000000', 136215277: '0.000003402912', 546587081934258176: '0.000000000000', 2391161556: '0.000000000000', 585777494: '0.000010208737', 546770821927010304: '0.333333333333'}
        client.db_close()
        assert js == influence_calculated

    def test_follow_relation_factor_user(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'nuclear' and depth < 2 limit -1")
        number_of_users = len(userlist);
        js = metrics.follow_relation_factor_user(userlist, number_of_users, 'nuclear')
        print(js)
        json = {}
        with open('tests/results/bigdata/bigdata.fr.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                json[row[0]] = row[1]        
        client.db_close()
        assert js == json

    def test_impact_user(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'nuclear' and depth < 2 limit -1")
        number_of_tweets = client.query("select count(*) as count from Tweet where topics containsText 'nuclear'")
        number_of_tweets = number_of_tweets[0].oRecordData['count']
        js = metrics.impact_user(userlist, number_of_tweets, 'nuclear')
        print(js)
        json = {}
        with open('tests/results/bigdata/bigdata.ui.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                json[row[0]] = row[1]
        client.db_close()
        assert js == json

    def test_voice_user(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'nuclear' and depth < 2 limit -1")
        js = metrics.voice_user(userlist, 'nuclear')
        print (js)
        json = {}
        with open('tests/results/bigdata/bigdata.voice_impact.asis.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                #print (row)
                json[row[0]] = {row[1], row[3]}         
        client.db_close()
        assert js == json

    def test_tweet_relevance(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        number_of_tweets = client.query("select count(*) as count from Tweet where topics containsText 'nuclear'")
        number_of_tweets = number_of_tweets[0].oRecordData['count']
        js = metrics.tweet_relevance(number_of_tweets, 'nuclear')
        client.db_close()
        print (js)
        relevance_calculated = {546860197587591168: 0.0, 546861511633682433: 0.0, 546861939037446144: 0.0}
        assert js == relevance_calculated

    def test_user_relevance(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'nuclear' and depth < 2 limit -1")
        js = metrics.user_relevance_score(userlist, 'nuclear')
        print (js)
        json = {}
        with open('tests/results/bigdata/bigdata.userrel.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                json[row[0]] = row[1]         
        client.db_close()
        assert js == json