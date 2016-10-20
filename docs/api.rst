Thank you for using the `{bootprint-swagger}
playground <http://bootprint.knappi.org/>`__

SCANER API
==========

Base URL: /api/v1, Version: 1.0.0

Default request content-types: application/json

Default response content-types: application/json

Schemes:

Summary
-------

Tag: users
~~~~~~~~~~

+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| Operation                                                                                                                                                                 | Description   |
+===========================================================================================================================================================================+===============+
| `GET /users/{userId} <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--users--userId--get>`__                       |               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /users/{userId}/emotion <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--users--userId--emotion-get>`__       |               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /users/{userId}/sentiment <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--users--userId--sentiment-get>`__   |               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /users/{userId}/metrics <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--users--userId--metrics-get>`__       |               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /users <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--users-get>`__                                         |               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /users/{userId}/network <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--users--userId--network-get>`__       |               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+

Tag: tweets
~~~~~~~~~~~

+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| Operation                                                                                                                                                                     | Description   |
+===============================================================================================================================================================================+===============+
| `GET /tweets/{tweetId} <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tweets--tweetId--get>`__                       |               |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `DELETE /tweets/{tweetId} <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tweets--tweetId--delete>`__                 |               |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /tweets/{tweetId}/history <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tweets--tweetId--history-get>`__       |               |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /tweets/{tweetId}/sentiment <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tweets--tweetId--sentiment-get>`__   |               |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /tweets/{tweetId}/emotion <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tweets--tweetId--emotion-get>`__       |               |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /tweets/{tweetId}/metrics <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tweets--tweetId--metrics-get>`__       |               |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /tweets <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tweets-get>`__                                           |               |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `POST /tweets <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tweets-post>`__                                         |               |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+

Tag: topics
~~~~~~~~~~~

+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| Operation                                                                                                                                                                 | Description   |
+===========================================================================================================================================================================+===============+
| `GET /topics <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--topics-get>`__                                       |               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /topics/{topicId} <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--topics--topicId--get>`__                   |               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /topics/{topicId}/network <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--topics--topicId--network-get>`__   |               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+

Tag: tasks
~~~~~~~~~~

+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| Operation                                                                                                                                                             | Description   |
+=======================================================================================================================================================================+===============+
| `GET /tasks <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tasks-get>`__                                     |               |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /tasks/{taskId} <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tasks--taskId--get>`__                   |               |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /tasks/emotiontask <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tasks-emotiontask-get>`__             |               |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /tasks/influencemetrics <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tasks-influencemetrics-get>`__   |               |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /tasks/updateusers <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tasks-updateusers-get>`__             |               |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
| `GET /tasks/getweetsbyid <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#operation--tasks-getweetsbyid-get>`__           |               |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+

Security
--------

Paths
-----

GET **/tasks**
~~~~~~~~~~~~~~

Tags:
`tasks <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tasks>`__

application/json

| 200 OK
| Tasks found and returned

GET **/tasks/emotiontask**
~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`tasks <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tasks>`__

`Uses default
content-types: <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#sw-default-produces>`__
application/json

| 200 OK
| Task running

GET **/tasks/getweetsbyid**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`tasks <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tasks>`__

`Uses default
content-types: <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#sw-default-produces>`__
application/json

| 200 OK
| Task running

GET **/tasks/influencemetrics**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`tasks <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tasks>`__

`Uses default
content-types: <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#sw-default-produces>`__
application/json

| 200 OK
| Task running

GET **/tasks/updateusers**
~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`tasks <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tasks>`__

`Uses default
content-types: <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#sw-default-produces>`__
application/json

| 200 OK
| Task running

GET **/tasks/{taskId}**
~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`tasks <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tasks>`__

+----------+----+--------+----------+----+
| taskId   |    | path   | string   |    |
+----------+----+--------+----------+----+

application/json

| 200 OK
| Task found and returned

GET **/topics**
~~~~~~~~~~~~~~~

Tags:
`topics <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-topics>`__

`Uses default
content-types: <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#sw-default-produces>`__
application/json

| 200 OK
| OK

`Topics <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Topics>`__

GET **/topics/{topicId}**
~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`topics <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-topics>`__

returns detailed info about relationships of a user

+-----------+----+--------+----------+----+
| topicId   |    | path   | string   |    |
+-----------+----+--------+----------+----+

`Uses default
content-types: <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#sw-default-produces>`__
application/json

| 200 OK
| OK

`Topics <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Topics>`__

GET **/topics/{topicId}/network**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`topics <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-topics>`__

returns detailed info about the users related to a topic

+-----------+----+--------+----------+----+
| topicId   |    | path   | string   |    |
+-----------+----+--------+----------+----+

`Uses default
content-types: <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#sw-default-produces>`__
application/json

| 200 OK
| OK

`Network <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Network>`__

GET **/tweets**
~~~~~~~~~~~~~~~

Tags:
`tweets <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tweets>`__

.. raw:: html

   <table>
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <tbody>
   <tr class="odd">
   <td align="left">fields</td>
   <td align="left"><p>Comma-separated list of fields to retrieve</p></td>
   <td align="left">query</td>
   <td align="left">string</td>
   <td align="left"></td>
   </tr>
   <tr class="even">
   <td align="left">limit</td>
   <td align="left"><p>Get only this many tweets per request</p></td>
   <td align="left">query</td>
   <td align="left">integer (int64)</td>
   <td align="left"></td>
   </tr>
   <tr class="odd">
   <td align="left">topic</td>
   <td align="left"><p>Only retrieve tweets related to a certain topic</p></td>
   <td align="left">query</td>
   <td align="left">string</td>
   <td align="left"></td>
   </tr>
   <tr class="even">
   <td align="left">sort_by</td>
   <td align="left"><p>Sort tweets using this criterion. Prepending a minus sign reverses the order. e.g. 'retweet_count'.</p></td>
   <td align="left">query</td>
   <td align="left">string</td>
   <td align="left"></td>
   </tr>
   </tbody>
   </table>

application/json

| 200 OK
| Tweets found and returned

`Tweets <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Tweets>`__

| 404 Not Found
| No Tweets found matching that query

POST **/tweets**
~~~~~~~~~~~~~~~~

Tags:
`tweets <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tweets>`__

Upload a tweet

`Uses default
content-types: <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#sw-default-consumes>`__
application/json

`Tweets\_Raw <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Tweets_Raw>`__

application/json

| 200 OK
| Uploaded

DELETE **/tweets/{tweetId}**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`tweets <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tweets>`__

Delete a Tweet

+-----------+----+--------+-------------------+----+
| tweetId   |    | path   | integer (int64)   |    |
+-----------+----+--------+-------------------+----+

application/json

| 200 OK
| Tweet deleted

| 404 Not Found
| Tweet not found

GET **/tweets/{tweetId}**
~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`tweets <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tweets>`__

.. raw:: html

   <table>
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <tbody>
   <tr class="odd">
   <td align="left">fields</td>
   <td align="left"><p>Comma-separated list of fields to include in the response.</p></td>
   <td align="left">query</td>
   <td align="left">string</td>
   <td align="left"></td>
   </tr>
   <tr class="even">
   <td align="left">tweetId</td>
   <td align="left"></td>
   <td align="left">path</td>
   <td align="left">integer (int64)</td>
   <td align="left"></td>
   </tr>
   </tbody>
   </table>

application/json

| 200 OK
| Tweet found and returned

`Tweets\_search <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Tweets_search>`__

| 404 Not Found
| Tweet not found

GET **/tweets/{tweetId}/emotion**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`tweets <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tweets>`__

+-----------+----+--------+-------------------+----+
| tweetId   |    | path   | integer (int64)   |    |
+-----------+----+--------+-------------------+----+

application/json

| 200 OK
| Tweet found and returned

| 404 Not Found
| Tweet not found

GET **/tweets/{tweetId}/history**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`tweets <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tweets>`__

.. raw:: html

   <table>
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <tbody>
   <tr class="odd">
   <td align="left">tweetId</td>
   <td align="left"></td>
   <td align="left">path</td>
   <td align="left">integer (int64)</td>
   <td align="left"></td>
   </tr>
   <tr class="even">
   <td align="left">since</td>
   <td align="left"><p>Time in seconds since EPOCH</p></td>
   <td align="left">query</td>
   <td align="left">integer</td>
   <td align="left"></td>
   </tr>
   <tr class="odd">
   <td align="left">until</td>
   <td align="left"><p>Time in seconds since EPOCH</p></td>
   <td align="left">query</td>
   <td align="left">integer</td>
   <td align="left"></td>
   </tr>
   </tbody>
   </table>

application/json

| 200 OK
| History

`Tweet\_history <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Tweet_history>`__

| 404 Not Found
| Tweet not found

GET **/tweets/{tweetId}/metrics**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`tweets <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tweets>`__

+-----------+----+--------+-------------------+----+
| tweetId   |    | path   | integer (int64)   |    |
+-----------+----+--------+-------------------+----+

application/json

| 200 OK
| Tweet found and returned

| 404 Not Found
| Tweet not found

GET **/tweets/{tweetId}/sentiment**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`tweets <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-tweets>`__

+-----------+----+--------+-------------------+----+
| tweetId   |    | path   | integer (int64)   |    |
+-----------+----+--------+-------------------+----+

application/json

| 200 OK
| Tweet found and returned

| 404 Not Found
| Tweet not found

GET **/users**
~~~~~~~~~~~~~~

Tags:
`users <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-users>`__

.. raw:: html

   <table>
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <tbody>
   <tr class="odd">
   <td align="left">fields</td>
   <td align="left"><p>Comma-separated list of fields to retrieve</p></td>
   <td align="left">query</td>
   <td align="left">string</td>
   <td align="left"></td>
   </tr>
   <tr class="even">
   <td align="left">limit</td>
   <td align="left"><p>Get only this many users per request</p></td>
   <td align="left">query</td>
   <td align="left">integer (int64)</td>
   <td align="left"></td>
   </tr>
   <tr class="odd">
   <td align="left">topic</td>
   <td align="left"><p>Only retrieve users related to a certain topic</p></td>
   <td align="left">query</td>
   <td align="left">string</td>
   <td align="left"></td>
   </tr>
   <tr class="even">
   <td align="left">sort_by</td>
   <td align="left"><p>Sort users using this criterion. Prepending a minus sign reverses the order. e.g. '-tweet_count'.</p></td>
   <td align="left">query</td>
   <td align="left">string</td>
   <td align="left"></td>
   </tr>
   </tbody>
   </table>

application/json

| 200 OK
| Users found and returned

`Users\_search <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Users_search>`__

GET **/users/{userId}**
~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`users <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-users>`__

.. raw:: html

   <table>
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <tbody>
   <tr class="odd">
   <td align="left">fields</td>
   <td align="left"><p>Comma-separated list of fields to include in the response.</p></td>
   <td align="left">query</td>
   <td align="left">string</td>
   <td align="left"></td>
   </tr>
   <tr class="even">
   <td align="left">userId</td>
   <td align="left"></td>
   <td align="left">path</td>
   <td align="left">integer (int64)</td>
   <td align="left"></td>
   </tr>
   </tbody>
   </table>

application/json

| 200 OK
| User found and returned

`Users <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Users>`__

| 404 Not Found
| User not found

GET **/users/{userId}/emotion**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`users <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-users>`__

+----------+----+--------+-------------------+----+
| userId   |    | path   | integer (int64)   |    |
+----------+----+--------+-------------------+----+

application/json

| 200 OK
| User found and returned

`Users <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Users>`__

| 404 Not Found
| User not found

GET **/users/{userId}/metrics**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`users <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-users>`__

+----------+----+--------+-------------------+----+
| userId   |    | path   | integer (int64)   |    |
+----------+----+--------+-------------------+----+

application/json

| 200 OK
| User found and returned

| 404 Not Found
| User not found

GET **/users/{userId}/network**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`users <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-users>`__

returns detailed info about relationships of a user

.. raw:: html

   <table>
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <col width="20%" />
   <tbody>
   <tr class="odd">
   <td align="left">userId</td>
   <td align="left"><p>user id of subject user</p></td>
   <td align="left">path</td>
   <td align="left">integer</td>
   <td align="left"></td>
   </tr>
   </tbody>
   </table>

`Uses default
content-types: <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#sw-default-produces>`__
application/json

| 200 OK
| OK

`Network <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Network>`__

GET **/users/{userId}/sentiment**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tags:
`users <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#tag-users>`__

+----------+----+--------+-------------------+----+
| userId   |    | path   | integer (int64)   |    |
+----------+----+--------+-------------------+----+

application/json

| 200 OK
| User found and returned

| 404 Not Found
| User not found

Schema definitions
------------------

Bounding\_box: object
~~~~~~~~~~~~~~~~~~~~~

| coordinates: number[][][]
| number[][]

number[]

number

type: string

CategoryEmotion: object
~~~~~~~~~~~~~~~~~~~~~~~

category: string

valence: number

Contributors: object
~~~~~~~~~~~~~~~~~~~~

id: integer

id\_str: string

screen\_name: string

Coordinates: object
~~~~~~~~~~~~~~~~~~~

| coordinates: number[]
| number

type: string

Emotions: object[]
~~~~~~~~~~~~~~~~~~

Emotions using the Onyx Ontology

object

extractedFrom: string

describesObject: string

describesObjectPart: string

describesObjectFeature: string

opinionCount: integer

| aggregatesOpinion: object,string[]
| object,string

| hasEmotion: object[]
| object

See VADEmotion and CategoryEmotion

| wasGeneratedBy: string
| ID of the analysis that generated this emotion

Entities: object
~~~~~~~~~~~~~~~~

hashtags: object[]
[Hashtags](https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Hashtags)

media: object[]
[Media](https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Media)

urls: object[]
[URL](https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/URL)

user\_mentions: object[]
[User\_Mention](https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/User_Mention)

Friendship: object
~~~~~~~~~~~~~~~~~~

source\_id: integer

source\_screen\_name: string

following: boolean

followed\_by: boolean

target\_id: integer

target\_screen\_name: string

Hashtags: object
~~~~~~~~~~~~~~~~

| indices: integer[]
| integer

text: string

History: object[]
~~~~~~~~~~~~~~~~~

object

time: number

value: number

Media: object
~~~~~~~~~~~~~

display\_url: string

expanded\_url: string

id: integer

id\_str: string

| indices: integer[]
| integer

media\_url: string

media\_url\_https: string

sizes:
`Sizes <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Sizes>`__

source\_status\_id: integer

source\_status\_id\_str: string

type: string

url: string

Metadata: object
~~~~~~~~~~~~~~~~

| url: string
| URL queried

| parameters: object
| Parameters used in the query

| timestamp: string
| Time when the query was performed

| count: integer
| Number of results returned

Network: object
~~~~~~~~~~~~~~~

links: object[]
[Friendship](https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Friendship)

Places: object
~~~~~~~~~~~~~~

| attributes: object
| object

bounding\_box:
`Bounding\_box <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Bounding_box>`__

country: string

country\_code: string

full\_name: string

id: string

name: string

place\_type: string

url: string

Raw\_Users: object
~~~~~~~~~~~~~~~~~~

contributors\_enabled: boolean

created\_at: string

default\_profile: boolean

default\_profile\_image: boolean

description: string

entities:
`Entities <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Entities>`__

favorites\_count: integer

follow\_request\_sent: boolean

geo\_enabled: boolean

id: integer

id\_str: string

is\_translator: boolean

lang: string

listed\_count: integer

location: string

name: string

notifications: boolean

profile\_background\_color: string

profile\_background\_image\_url: string

profile\_background\_image\_url\_https: string

profile\_background\_tile: string

profile\_banner\_url: string

profile\_image\_url: string

profile\_image\_url\_https: string

profile\_link\_color: string

profile\_sidebar\_border\_color: string

profile\_sidebar\_fill\_color: string

profile\_text\_color: string

profile\_use\_background\_image: boolean

protected: boolean

screen\_name: string

show\_all\_inline\_media: boolean

status:
`Tweets <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Tweets>`__

statuses\_count: integer

time\_zone: string

url: string

utc\_offset: integer

verified: boolean

withheld\_in\_countries: string

withheld\_scope: string

Sentiments: object[]
~~~~~~~~~~~~~~~~~~~~

Sentiments using the Marl Ontology

object

hasPolarity: string

polarityValue: number

extractedFrom: string

describesObject: string

describesObjectPart: string

describesObjectFeature: string

| opinionCount: integer
| Used for AggregatedOpinion/Sentiment

| aggregatesOpinion: object,string[]
| object,string

algorithmConfidence: number

| wasGeneratedBy: string
| ID of the analysis that generated this sentiment

Size: object
~~~~~~~~~~~~

h: integer

resize: string

w: integer

Sizes: object
~~~~~~~~~~~~~

thumb:
`Size <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Size>`__

large:
`Size <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Size>`__

medium:
`Size <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Size>`__

small:
`Size <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Size>`__

Topic: object
~~~~~~~~~~~~~

A topic

id: string

last\_tweet: string

tweet\_count: integer

user\_count: integer

Topics: object[]
~~~~~~~~~~~~~~~~

List of topics

`Topic <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Topic>`__

Tweet\_history: object
~~~~~~~~~~~~~~~~~~~~~~

| id: integer
| Tweet ID

retweet\_count:
`History <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/History>`__

favourite\_count:
`History <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/History>`__

Tweet\_metrics: object
~~~~~~~~~~~~~~~~~~~~~~

| relevance: number
| Tweet Relevance Score: shows the relevancy of a tweet based on the
“voice” of the original user and the impact of the users that have
posted, retweeted or replied to this tweet

| retweetCount: integer
| Number of Retweets this Tweet has

| favouriteCount: integer
| Number of Favourite marks this Tweet has

| lastUpdated: string
| Timestamp of last metrics collection

Tweets:
~~~~~~~

metrics:
`Tweet\_metrics <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Tweet_metrics>`__

sentiments:
`Sentiments <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Sentiments>`__

emotions:
`Emotions <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Emotions>`__

Tweets\_Raw: object
~~~~~~~~~~~~~~~~~~~

| topics: string[]
| string

contributors: object[]
[Contributors](https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Contributors)

coordinates:
`Coordinates <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Coordinates>`__

created\_at: string

entities:
`Entities <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Entities>`__

favorite\_count: integer

favorited: boolean

filter\_level: string

id: integer

id\_str: string

in\_reply\_to\_screen\_name: string

in\_reply\_to\_status\_id: integer

in\_reply\_to\_status\_id\_str: string

in\_reply\_to\_user\_id: integer

in\_reply\_to\_user\_id\_str: string

lang: string

place:
`Places <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Places>`__

possibly\_sensitive: boolean

quoted\_status\_id: integer

quoted\_status\_id\_str: string

quoted\_status: object

| scopes: object
| object

retweet\_count: integer

retweeted\_status: object

source: string

text: string

truncated: string

| user\_id: number
| User ID

withheld\_copyright: boolean

| withheld\_countries: string[]
| string

withheld\_scope: string

Tweets\_search: object
~~~~~~~~~~~~~~~~~~~~~~

statuses: object[]
[Tweets](https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Tweets)

metadata:
`Metadata <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Metadata>`__

URL: object
~~~~~~~~~~~

display\_url: string

expanded\_url: string

| indices: integer[]
| integer

url: string

User\_history: object
~~~~~~~~~~~~~~~~~~~~~

Work in progress. Not implemented yet

| id: integer
| User ID

followers:
`History <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/History>`__

following:
`History <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/History>`__

User\_Mention: object
~~~~~~~~~~~~~~~~~~~~~

id: integer

id\_str: string

| indices: integer[]
| integer

name: string

screen\_name: string

User\_metrics: object
~~~~~~~~~~~~~~~~~~~~~

| followers: integer
| Number of users following this user

| following: integer
| Number of users this user is following

| followRatio: number
| Ratio followers/following

| hIndexFav: number
| h-index calculated from the number of Favorite marks of the last 100
Tweets of the user.
`https://en.wikipedia.org/wiki/H-index <https://en.wikipedia.org/wiki/H-index>`__

| hIndexRt: number
| h-index calculated from the number of Retweets of the last 100 Tweets
of the user.
`https://en.wikipedia.org/wiki/H-index <https://en.wikipedia.org/wiki/H-index>`__

| replyRatio: number
| Ratio of user's tweets that are a reply to other users

| repliedRatio: number
| Ratio of user's tweets that receive a reply

| influence: number
| User Influence Score: measures the “amount of attention” that a user
receives from the rest of the users

| openinfluence: number
| User Influence calculated using the OpenInfluence algorithm:
`https://en.paradigmadigital.com/dev/openinfluence/ <https://en.paradigmadigital.com/dev/openinfluence/>`__

| relevance: number
| User Relevance Score: This metric is the combined score of the Tweet
Rate Score, the User Influence Score and the Follow Relation Factor

| voice: number
| User Voice: measures the ability of a user to posts or retweets
influential tweets

| impact: number
| User Impact: measures the ability of a user to improve the relevance
of a tweet depending on their influence

| tweetRatio: number
| Tweet ratio: Measures the proportion of the tweets published by the
user which are related to the topic

| followRelationScore: number
| Follow Relation Score: Measures the cuality of the relations of this
sers with other users of the network

| lastUpdated: string
| Timestamp of last metrics collection

Users:
~~~~~~

metrics:
`User\_metrics <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/User_metrics>`__

Users\_search: object
~~~~~~~~~~~~~~~~~~~~~

users: object[]
[Users](https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Users)

metadata:
`Metadata <https://bootprint.knappi.org/bootprint/2daa56ed602e55181b5710d38bdb06bec4836553/bundle.html#/definitions/Metadata>`__

VADEmotion: object
~~~~~~~~~~~~~~~~~~

valence: number

arousal: number

dominance: number

\\\\\\
