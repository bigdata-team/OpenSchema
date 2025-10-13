#!/bin/bash

function handle_interrupt {
    echo "Script interrupted. Exiting..."
    exit 0
}

trap handle_interrupt SIGINT

while :
do
	docker compose -f ./docker/docker-compose-service.yaml logs -f
	sleep 1
done

