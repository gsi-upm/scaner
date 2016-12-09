
API Usage
=========

POST /tweets
------------

**Example request**:
  .. sourcecode:: http
       
     POST /api/v1/tweets/ HTTP/1.1 
     Host: localhost 
     'Content-Type': 'application/json',  
     'Accept': 'application/json'

**Example respond**: 
  .. sourcecode:: http 
     
     HTTP/1.1 200 OK 
     'Content-Type':'application/json', 
     'Vary':'Accept'

      { 
     	"metadata": { "parameters": {}, 
                    "url": "http://localhost:5000/api/v1/tweets"}, 
     	"result": "Tweet added to DB."
      }

GET /tweets
-----------

**Example request**:
  .. sourcecode:: http
     
     GET /api/v1/tweets?limit=1 HTTP/1.1 
     Host: localhost 
     'Accept': 'application/json'

**Example respond**: 
  .. sourcecode:: http
     
     HTTP/1.1 200 OK 
     'Content-Type':'application/json'
     'Vary':'Accept'

    {
      "metadata": {
        "count": 20,
        "parameters": {
          
        },
        "url": "http://localhost:5000/api/v1/tweets"
      },
      "statuses": [
        {
          "created_at": "Mon Dec 15 23:29:35 +0000 2014",
          "entities": {
            "hashtags": [
              
            ],
            "symbols": [
              
            ],
            "urls": [
              {
                "display_url": "bit.ly/1AeESXb",
                "expanded_url": "http://bit.ly/1AeESXb",
                "indices": [
                  19,
                  41
                ],
                "url": "http://t.co/1JWX4VDvmz"
              }
            ],
            "user_mentions": [
              
            ]
          },
          "id": 000000000000,
          "id_str": "000000000000",
          "lang": "ja",
          "metadata": {
            "iso_language_code": "ja",
            "result_type": "recent"
          },
          "text": " http://t.co/1JWX4VDvmz",
          "timestamp_ms": 1418686175.0,
          "topics": [
            "bigdata"
          ],
          "user": {
            "created_at": "Tue Sep 02 01:27:55+0000 2014",
            "followers_count": 7254,
            "following": null,
            "friends_count": 7277,
            "id": 0000000000,
            "id_str": "0000000000",
            "lang": "ja",
            "protected": 0,
            "screen_name": "*******",
            "statuses_count": 9328
          }
        }
      ]
    }

**Query parameters**: 
  - query (f) fields: Comma-separated list of fields to retrieve e.g 'screen_name' 'following' 
  - query (l) limit: Get only this many users per request by default limit is 20 tweets 
  - query (t) topic: Only retrieve users related to a certain topic e.g 'LaboralKutxa' 
  - query (s) sort_by: Sort users using this criterion. Prepending a minus sign reverses the order. e.g. '- tweet_count'.

GET /tweets/{tweetId}/metrics
-----------------------------

**Example request**:
  .. sourcecode:: http
     
     GET /api/v1/tweets/{tweetId}/metrics HTTP/1.1 
     Host: localhost 
     'Content-Type': 'application/json'  
     'Accept': 'application/json'``

**Example respond**: 
  .. sourcecode:: http 
     
     HTTP/1.1 200 OK 
     'Content-Type':'application/json' 
     'Vary':'Accept'

    {
      "metadata": {
        "parameters": {
          
        },
        "url": "http://localhost:5000/api/v1/tweets/0000000000000/metrics"
      },
      "result": {
        "complete": true,
        "date": "2016-12-07",
        "id": 0000000000000,
        "influence": 0.496603800169,
        "lastMetrics": true,
        "relevance": 0.10244804983,
        "timestamp": 1481107250.4926267,
        "topic": "bigdata"
      }
    }

**Path parameters**: 
  - path (t) tweetId (required):Tweet id to filter by

GET /tweets/{tweetId}/history
-----------------------------

**Example request**:
  .. sourcecode:: http
     
     GET /api/v1/tweets/{tweetId}/history HTTP/1.1 
     Host: localhost 
     'Content-Type': 'application/json',  
     'Accept': 'application/json'``

**Example respond**: 
  .. sourcecode:: http

     HTTP/1.1 200 OK 
     'Content-Type':'application/json' 
     'Vary':'Accept'

    {
      "metadata": {
        "parameters": {
          
        },
        "url": "http://localhost:5000/api/v1/tweets/000000000000000/history"
      },
      "result": [
        {
          "complete": true,
          "date": "2016-12-07",
          "id": 000000000000000,
          "influence": 0.496603800169,
          "lastMetrics": true,
          "relevance": 0.10244804983,
          "timestamp": 1481107250.4926267,
          "topic": "bigdata"
        },
        {
          "complete": true,
          "date": "2016-12-05",
          "id": 000000000000000,
          "influence": 0.0,
          "lastMetrics": false,
          "relevance": 0.0,
          "timestamp": 1480940543.4212337,
          "topic": "bigdata"
        }
      ]
    }

**Path parameters**:
  - path (t) tweetId (required):Tweet id to filter by

GET /users
----------

**Example request**:
  .. sourcecode:: http
     
     GET /api/v1/users?limit=3 HTTP/1.1 
     Host: localhost 
     'Content-Type': 'application/json'  
     'Accept': 'application/json'``

**Example respond**:  
  .. sourcecode:: http
     
     HTTP/1.1 200 OK 
     'Content-Type':'application/json'
     'Vary':'Accept'
    {
      "metadata": {
        "count": 3,
        "parameters": {
          
        },
        "url": "http://localhost:5000/api/v1/users"
      },
      "users": [
        {
          "community": 1156,
          "created_at": "Mon Nov 10 16:10:39 +0000 2014",
          "followers_count": 7,
          "friends_count": 23,
          "id": 0,
          "id_str": "0",
          "lang": "ru",
          "protected": "0",
          "screen_name": "*****",
          "statuses_count": 38,
          "topics": [
            "bigdata"
          ]
        },
        {
          "community": 560,
          "created_at": "Mon Nov 10 19:57:30 +0000 2014",
          "followers_count": 3,
          "friends_count": 12,
          "id": 1,
          "id_str": "1",
          "lang": "ru",
          "protected": "0",
          "screen_name": "*****",
          "statuses_count": 56,
          "topics": [
            "bigdata"
          ]
        },
        {
          "community": 4,
          "created_at": "Sun Jan 17 16:12:59 +0000 2010",
          "followers_count": 936,
          "friends_count": 1154,
          "id": 2,
          "id_str": "2",
          "lang": "ja",
          "protected": "0",
          "screen_name": "****",
          "statuses_count": 20637,
          "topics": [
            "bigdata"
          ]
        }
      ]
    }

**Query parameters**: 
  - query (f) fields: Comma-separated list of fields to retrieve e.g 'screen_name' 'following' 
  - query (l) limit: Get only this many users per request by default limit is 20 tweets 
  - query (t) topic: Only retrieve users related to a certain topic e.g 'LaboralKutxa' 
  - query (s) sort_by: Sort users using this criterion. Prepending a minus sign reverses the order. e.g. '- tweet_count'.

GET /users/{userId}/metrics
---------------------------

**Example request**:
  .. sourcecode:: http
     
     GET /api/v1/users/{userId}/metrics HTTP/1.1 
     Host: localhost 
     'Content-Type': 'application/json'  
     'Accept': 'application/json'``

**Example respond**:
  .. sourcecode:: http 
     
     HTTP/1.1 200 OK 
     'Content-Type':'application/json' 
     'Vary':'Accept'

    {
      "metadata": {
        "parameters": {},
        "url": "http://localhost:5000/api/v1/users/59390872/metrics"
      },
      "result": {
        "complete": true,
        "date": "2016-12-07",
        "followRelationScore": 0.140941982233,
        "followers": 43017,
        "following": 43445,
        "id": 59390872,
        "impact": 0.000002767175,
        "influence": 1,
        "influenceUnnormalized": 0.00499198376,
        "lastMetrics": true,
        "relevance": 2.105912,
        "statuses_count": 39233,
        "timestamp": 1481114116.3879638,
        "topic": "bigdata",
        "tweetRatio": 0.00015293248,
        "voice": 0.030976330457,
        "voice_r": 0.00000003215
      }
    }

**Path parameters**: 
  - path (t) userId (required):User id to filter by

GET /users/{userId}/network
---------------------------

**Example request**:
  .. sourcecode:: http
     
     GET /api/v1/users/{userId}/network 
     HTTP/1.1 Host: localhost 
     'Content-Type': 'application/json'  
     'Accept': 'application/json'

**Example respond**:
  .. sourcecode:: http 
     HTTP/1.1 200 OK 
     'Content-Type':'application/json' 
     'Vary':'Accept'
      {
        "metadata": {
          "parameters": {
            
          },
          "url": "http://localhost:5000/api/v1/users/59390872/network"
        },
        "result": [
          {
            "id": 1
          },
          {
            "id": 2
          },
          {
            "id": 4
          },
          {
            "id": 5
          },
          {
            "id": 7
          },
          {
            "id": 94
          },
          {
            "id": 132
          },
          {
            "id": 464
          }
        ]
      }

GET /communities
----------------

**Example request**:
  .. sourcecode:: http
     
     GET /api/v1/communities/ HTTP/1.1 
     Host: localhost 
     'Content-Type': 'application/json'  
     'Accept': 'application/json'

**Example respond**:   
  .. sourcecode:: http
     
     HTTP/1.1 200 OK 
     'Content-Type':'application/json' 
     'Vary':'Accept'

     {
      "communities": [
        {
          "emotion": "joy",
          "id": 0,
          "sentiment": "positive",
          "user_count": 12
        },
        {
          "emotion": "joy",
          "id": 1,
          "sentiment": "positive",
          "user_count": 32
        },
        {
          "emotion": "joy",
          "id": 2,
          "sentiment": "positive",
          "user_count": 8
        }
      ],
      "metadata": {
        "count": 3,
        "parameters": {
          
        },
        "url": "http://localhost:5000/api/v1/communities"
      }
    }

**Query parameters**: 
  - query (f) fields: Comma-separated list of fields to retrieve e.g 'screen_name' 'following' 
  - query (l) limit: Get only this many users per request by default limit is 20 tweets 
  - query (t) topic: Only retrieve users related to a certain topic e.g 'LaboralKutxa' 
  - query (s) sort_by: Sort users using this criterion. Prepending a minus sign reverses the order. e.g. '- tweet_count'.

Adding more tweets for the same topic
-------------------------------------

Once Scaner has calculated the metrics for a certain topic, the tool
allows to retrieve instant information of relevance of a tweet in that
topic.

**Example request**:
  .. sourcecode:: http
     
     POST /api/v1/tweets/ HTTP/1.1 
     Host: localhost 
     'Content-Type': 'application/json' 
     'Accept': 'application/json'``

**Example respond**: 
  .. sourcecode:: http
     
     HTTP/1.1 200 OK 
     'Content-Type':'application/json' 
     'Vary':'Accept'

    {
      "metadata": {
        "parameters": {
          
        },
        "url": "http://localhost:5000/api/v1/tweets"
      },
      "result": {
        "result": "Tweet added to DB",
        "topic": "bigdata",
        "tweet_relevance": "0.010244804983"
      }
    }