#Scaner
##Arquitecture
![alt tag](https://raw.githubusercontent.com/gsi-upm/scaner/newdata/overview.png?token=AKvRCZVCM46LZWHwF_50RvQPtwBSjtzaks5X389rwA%3D%3D)

## Installation
Firstly you have to install [Docker](https://docs.docker.com/engine/installation/) and Docker Compose. This can be easily installed with [pip](https://pip.pypa.io/en/stable/installing/):
```
$ pip install docker-compose
```

Now, clone the repository into your local system
```
$ git clone http://github.com/gsi-upm/scaner
```
Use Docker Compose to build the application:

```
$ cd scaner
$ docker-compose build
```
Then, it is necessary to run **OrientDB**
```
$ ./populate_schema.sh
```
Finally, we run the application
```
$ docker-compose up
```
Scaner application it is now available on port **5000**
