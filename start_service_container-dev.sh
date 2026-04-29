#!/bin/sh
docker run -p 8000:8000 --network owlcam-network --env-file .env --name owlcam-service owlcamservice-prod