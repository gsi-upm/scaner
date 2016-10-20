What is Scaner?
--------------

SCANER: Social Context Analysis aNd Emotion Recognition is a platform to collect and analyse social context, i.e context of users and content in social media. In particular, Scaner detects possible influencers and assess their relevance and impact capabilities in a given topic.

The platform is able to extract and process social media information data from Twitter, allowing us to analyse and process different metrics from tweets and users. To perform the test of the platform, it includes models of users and tweets. It creates the appropriate relationships between users and their related tweets, it calculates their influences and makes this information available through a REST API.

Social Context
==============

There are two main components in social context: users and content. Any information from the social network that is not present in the bare textual content could be considered part of its social context. Scaner calculates metrics to include richer aspects from the social network, exploiting he graph of relationships and interactions between users and content. Some of these aspects, the more general ones, are already provided by the social network site through its API, such as the number of mentions, favourites or replies. More specific or intensive metrics need to be computed by third parties.


Architecture
============

The modular architecture of Scaner allows retrieving, storing and processing large amounts of information. The independent task system and API further contribute to decouple the modules in the platform. 

* OrientDB stores all the amount of data that we needed and easily edges the information to create graphs.
* The crawler has been able to extract the necessarry information from Twitter, being only limited by the Twitter API rate limit. Scaner uses `bitter <https://github.com/balkian/bitter>`_ to implement this task.
* The task manager process all this information.


.. image:: overview.png
  :height: 800px
  :width: 800px
  :scale: 100 %
  :align: center
