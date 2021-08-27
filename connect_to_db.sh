#!/bin/bash
#get default docker project prefix from dir
#get container id from grep match
DOCKER_DB_ID=$(docker ps --format="{{.Names}} {{.ID}}" | grep "${PWD##*/}_db" | cut -d' ' -f2)
docker exec -it $DOCKER_DB_ID bash -c "psql -d rosetta -U superuser"
