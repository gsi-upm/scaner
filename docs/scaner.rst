What is Scaner?
--------------

SCANER: Social Context Analysis aNd Emotion Recognition is a platform to collect and analyse social context, i.e context of users and content in social media. 

The platform is able to extract and process social media information data from Twitter, allowing us to analyse and process different metrics from tweets and users. To perform the test of the platform, it includes models of users and tweets. It creates the appropriate relationships between users and their related tweets, it calculates their influences and makes this information available through a REST API.




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


More
====

For more information visit http://scaner.readthedocs.io/en/latest/

Acknowledgement
...............

This development has been partially funded by the European Union through the MixedEmotions Project (project number H2020 655632), as part of the `RIA ICT 15 Big data and Open Data Innovation and take-up` programme.

.. image:: ../img/me.png
   :target: http://mixedemotions-project.eu
   :height: 100px
   :alt: MixedEmotions Logo

.. image:: ../img/eu-flag.jpg
   :height: 100px
   :target: http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/index.html

.. image:: ../http://vps161.cesvima.upm.es/images/stories/logos/gsi.png
   :alt: GSI Logo
   