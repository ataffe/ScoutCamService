#!/bin/sh
docker run -p 8000:8000 --network scoutcam-network --env-file .env --name scoutcam-service scoutcamservice-prod