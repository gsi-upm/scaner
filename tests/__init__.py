import unittest
import pyorient
import json
import random


import scaner.tasks as task


class UnitTests(unittest.TestCase):

    def test_user_metrics(self):
        js = task.get_user_metrics(84333477)
        assert  all (k in js for k in ('influenceUnnormalized','influence','voice_r','tweetRatio','lastMetrics','relevance','statuses_count','complete','following','impact','id','voice','date','followers'))

    def test_user_in_DB(self):
    	js = task.user(2359753596)
    	assert 'id' in js

    def test_user_not_in_DB(self):
        js = task.user(random.randint(0, 20))
        assert js == "User not found in DB"

    def test_user_network(self):
        js = task.user_network(2359753596)
        network = [{'id': 748645976647270404}, {'id': 751365783452811264}, {'id': 751385737728237568}, {'id': 748754982564794368}, {'id': 751376008784252928}, {'id': 751394562422243328}]
        assert js == network

    def test_tweet_in_DB(self):
        js = task.tweet(748754982564794368)
        assert 'id' in js

    def test_tweet_not_in_DB(self):
        js = task.tweet(random.randint(0, 20))
        assert js == "Tweet not found in DB"

    def test_tweet_metrics(self):
        js = task.get_tweet_metrics(748754982564794368)
        assert  all (k in js for k in ('date','influence','lastMetrics','relevance','complete','id','topic','timestamp'))
    def test_tweet_history(self):
        js = task.tweet_history(748754982564794368)
        for i in js:
            if not all (k in i for k in ('date','influence','lastMetrics','relevance','complete','id','topic','timestamp')):
                assert False
        assert True