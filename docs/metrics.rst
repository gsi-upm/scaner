Metrics
-------

Internally, metrics are classified in two different types: direct and indirect metrics. 

Direct metrics
==============

Direct metrics are directly obtainable from the extracted data, such as the number of followers
a user has. The Social Context Analysis module obtains direct metrics as soon as new
social media content is stored in the database, and these metrics are updated when new
information arrive. For instance, the Social Context module is configured to refetch general
information about users periodically, so these metrics would be updated as well.

Indirect metrics
================

Indirect metrics are obtained through data processing, for example User Influence. These
metrics are calculated periodically, as they have a high processing cost and require accessing
all the information in the database.

User relevance
**************

We define the user relevance score based in the tweet rate, the user influence and follow relation score of each user.

Tweet Rate (TR) score
~~~~~~~~~~~~~~~~~~~~~

This metric measures the proportion of tweets related to the topic that a user posts or retweets.
Some of the topic-related users usually retweet tweets relevant to the topic originally posted by others, which means they play a role
of “filter” searching for valuable relevant tweets and sharing them with their followers.

User Influence (UI) score and Tweet Influence (TI) score
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

How much each tweet is paid attention to by others is measured according to the retweet and reply activities and the follow relation.
Based on this idea, we define not only the UI score of each user but also “tweet influence (TI) score” of each tweet.
The UI score of each user is calculated using the TI score of the user’s tweets and retweets, and the TI score of each tweet 
is calculated using the UI score of users who pay attention to the tweet.

Follow Relation (FR) score
~~~~~~~~~~~~~~~~~~~~~~~~~~

A reference graph consisting of user nodes and directed edges each of which connects two of the user nodes, called “follow relation graph”, 
is created from the follow relation.

Tweet relevance
***************

They describe a method for finding relevant tweets to the target topic. 

Voice and Impact score calculation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to judge the relevance of each tweet to the target topic, we have the following assumptions about tweets relevant to 
the topic (relevant tweets).

1. The relevant tweets are posted or retweeted by the topic-related users.

2. The relevant tweets are paid attention to (retweeted or replied to) by many topic-related users.

The Impact score is used for the estimation based on the first idea, and the Voice score is used for the estimation based on the second idea.

Tweet Ranking
~~~~~~~~~~~~~

The tweet relevance score of each tweet is calculated from the Voice score and the Impact score, then select the top-M tweets ranked
by the tweet relevance score as the tweets relevant to the target topic.