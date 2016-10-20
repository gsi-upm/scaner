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

Tweet Rate (TR) Score
=====================

User Influence (UI) Score
=========================

Follow Relation (FR) Score
==========================