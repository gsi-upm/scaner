What is Scaner?
--------------

SCANER: Social Context Analysis aNd Emotion Recognition is a platform to collect and analyse social context, i.e context of users and content in social media. In particular, Scaner detects possible influencers and assess their relevance and impact capabilities in a given topic.

The overall goal of the reference implementation Scaner is easing the adoption of the proposed linked data model for sentiment and emotion analysis services, so that services from different providers become interoperable. With this aim, the design of the reference implementation has focused on its extensibility and reusability. 

A modular approach allows organizations to replace indiv

Specifications
==============

The model used in Senpy is based on the following specifications:

* Marl, a vocabulary designed to annotate and describe subjetive opinions expressed on the web or in information systems.
* Onyx, which is built one the same principles as Marl to annotate and describe emotions, and provides interoperability with Emotion Markup Language.
* NIF 2.0, which defines a semantic format and APO for improving interoperability among natural language processing services

Architecture
============

The main component of a sentiment analysis service is the algorithm itself. However, for the algorithm to work, it needs to get the appropriate parameters from the user, format the results according to the defined API, interact with the user whn errors occur or more information is needed, etc.

Senpy proposes a modular and dynamic architecture that allows:

* Implementing different algorithms in a extensible way, yet offering a common interface.
* Offering common services that facilitate development, so developers can focus on implementing new and better algorithms.

The framework consists of two main modules: Senpy core, which is the building block of the service, and Senpy plugins, which consist of the analysis algorithm. The next figure depicts a simplified version of the processes involved in an analysis with the Senpy framework.

.. image:: senpy-architecture.png
  :height: 400px
  :width: 800px
  :scale: 100 %
  :align: center
