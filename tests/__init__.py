import unittest
import pyorient
import json
import random


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
        #print(len(js))
        network = 12372
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
        metrics_calculated = {85727936: '0.000002603150', 15978752: '0.222222222222', 585777494: '0.000031971354', 356195126: '0.333333333333', 136215277: '0.000022684996', 89049149: '0.000000000000'}
        client.db_close()
        assert js == metrics_calculated
    
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
        influence_calculated = {85727936: '0.000002603150', 15978752: '0.500000000000', 585777494: '0.000031971354', 356195126: '0.333333333333', 136215277: '0.000022684996', 89049149: '0.000000000000'}
        client.db_close()
        assert js == influence_calculated

    def test_follow_relation_factor_user(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'nuclear' and depth < 2 limit -1")
        number_of_users = len(userlist);
        js = metrics.follow_relation_factor_user(userlist, number_of_users, 'nuclear')
        #print(js)
        follow_relation_calculated = {85727936: '0.499999999999', 15978752: '1.000000000000', 585777494: '0.999999999999', 356195126: '0.749999999999', 136215277: '0.499999999999', 89049149: '0.499999999999'}
        client.db_close()
        assert js == follow_relation_calculated

    def test_impact_user(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'nuclear' and depth < 2 limit -1")
        number_of_tweets = client.query("select count(*) as count from Tweet where topics containsText 'nuclear'")
        number_of_tweets = number_of_tweets[0].oRecordData['count']
        js = metrics.impact_user(userlist, number_of_tweets, 'nuclear')
        #print(js)
        impact_user_calculated = {85727936: '0.000000000000', 15978752: '0.000000000000', 585777494: '0.000000000000', 356195126: '0.000000000000', 136215277: '0.000000000000', 89049149: '0.000000000000'}
        client.db_close()
        assert js == impact_user_calculated

    def test_voice_user(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        userlist = client.query("select id, followers_count, friends_count, statuses_count, topics from User where pending = false and topics containsText 'nuclear' and depth < 2 limit -1")
        js = metrics.voice_user(userlist, 'nuclear')
        #print (js)
        voice_user_calculated = {85727936: {'0.000000000000'}, 15978752: {'0.219433508141'}, 585777494: {'0.000000000000', '0.666666666666'}, 356195126: {'0.000000000000'}, 136215277: {'0.000000000000', '0.222222222222'}, 89049149: {'0.000000000000'}}
        client.db_close()
        assert js == voice_user_calculated

    def test_tweet_relevance(self):
        client = pyorient.OrientDB("orientdb_test", 2424)
        session_id = client.connect("root", "root")
        client.db_open("mixedemotions", "admin", "admin")
        number_of_tweets = client.query("select count(*) as count from Tweet where topics containsText 'nuclear'")
        number_of_tweets = number_of_tweets[0].oRecordData['count']
        js = metrics.tweet_relevance(number_of_tweets, 'nuclear')
        client.db_close()
        #print (js)
        relevance_calculated = {546587081934258176: 0.0, 546770821927010304: 0.0, 546861511633682433: 0.0, 546860197587591168: 0.0, 546796939535065088: 0.0, 546861939037446144: 0.0, 546857890833641472: 0.0}
        assert js == relevance_calculated