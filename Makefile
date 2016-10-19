NAME=scaner
REPO=gsiupm
VERSION=master

build:
	docker build -t '$(REPO)/$(NAME):$(VERSION)' -f tests/Dockerfile .;

test: build

	docker network create -d bridge my-net
	docker run -d --name orientdb_test -p 2425:2424 -p 2481:2480 -v ~/Desktop/scaner/tests/DB/databases:/orientdb/databases -v ~/Desktop/scaner/tests/DB/config:/orientdb/config -e ORIENTDB_ROOT_PASSWORD=rootpwd --network=my-net orientdb 
	docker run --rm -w /usr/src/app/ --entrypoint=/usr/local/bin/python --network=my-net -ti '$(REPO)/$(NAME):$(VERSION)' setup.py test ;

clean:

	docker rm -f orientdb_test
	docker network rm my-net

.PHONY: test build

