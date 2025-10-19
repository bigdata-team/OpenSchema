#!/bin/bash

#################################################################################################
#################################################################################################
#################################################################################################
check_error() {
	RESULT=`echo $?`
	if [ $RESULT -ne 0 ]; then
		echo ""
		echo ""
		echo "??????????????????????????????????????????????????????????????"
		echo "[ERROR] Error is detected. [${RESULT}]"
		echo
		echo
		exit 1
	fi
}

#################################################################################################
#################################################################################################
#################################################################################################
#docker compose --env-file .env.dev -f docker-compose-kafka.yaml down
#docker compose --env-file .env.dev -f docker-compose-kafka.yaml build
#docker compose --env-file .env.dev -f docker-compose-kafka.yaml up -d

#docker compose --env-file .env.dev -f docker-compose-infra.yaml down
#docker compose --env-file .env.dev -f docker-compose-infra.yaml build
#docker compose --env-file .env.dev -f docker-compose-infra.yaml up -d
###sleep 10

#docker compose --env-file .env.dev -f docker-compose-web.yaml down
#check_error
#docker compose --env-file .env.dev -f docker-compose-web.yaml build # --no-cache
#check_error
#docker compose --env-file .env.dev -f docker-compose-web.yaml up -d
#check_error

#docker compose --env-file .env.dev -f docker-compose-service.yaml down
#check_error
#docker compose --env-file .env.dev -f docker-compose-service.yaml build # --no-cache
#check_error
#docker compose --env-file .env.dev -f docker-compose-service.yaml up -d
#check_error

docker compose --env-file .env.dev -f docker-compose-ui.yaml down
check_error
###### DOCKER_BUILDKIT=0 
docker compose --env-file .env.dev -f docker-compose-ui.yaml build # --no-cache
check_error
docker compose --env-file .env.dev -f docker-compose-ui.yaml up -d
check_error
