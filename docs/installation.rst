Installation
------------
Scaner requires docker and docker-compose to work. You can download Docker `here <https://docs.docker.com/engine/installation/>`_

Docker-compose can be easily installed through pip.

.. code:: bash

   $ pip install docker-compose

Building Scaner
***************
   
First of all, you need to clone the Github repository:
 
.. code:: bash

   $ git clone git@github.com:gsi-upm/scaner
   $ cd scaner

Once cloned, we need to build the docker image:

.. code:: bash

    $ docker-compose build

Then, it is necessary to populate **OrientDB** schema.

.. code:: bash

    $ ./populate_schema.sh

Running Scaner
**************

Now the image is ready to run:

.. code:: bash

    $ docker-compose up  
