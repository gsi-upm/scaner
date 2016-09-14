#!/bin/bash
docker run --rm -ti \
	-v "$(pwd)/DB/databases:/orientdb/databases" \
	-v "$(pwd)/DB/config:/orientdb/config" \
	-v "$(pwd)/createmydb.sh:/createmydb.sh" \
	orientdb \
	/orientdb/bin/console.sh /createmydb.sh
