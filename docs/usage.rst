Usage
-----
Adding data to Scaner
=====================

Once Scaner is running in your computer, you can add tweets to the system in order to be analyzed. We have implemented a script to execute this task. You need to specify the path of the directory where the tweets you want to analyze are. This tweets should be in JSON format.

.. code:: bash
        
        python3 populate_db.py  {$path to the tweets}


This script has also more features that are explained if you type

.. code:: bash

        python3 populate_db.py --h

Finding social context for tweets
=================================
