#!/bin/sh
if ! docker network inspect owlcam-network >/dev/null 2>&1; then
  docker network create owlcam-network
fi
docker run -e POSTGRES_DB=owlcamservicedb \
 -p :5432:5432 \
 -e POSTGRES_USER=appuser \
 -e POSTGRES_PASSWORD=lYr3KCPu6QFr8W9KHcRF7gAK2Wfp \
 --name owlcam-postgres \
 --network owlcam-network postgres