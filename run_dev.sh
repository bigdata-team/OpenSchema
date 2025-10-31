#!/bin/bash

##### go to web folder
##### cd src/web
#####
##### cp -R src/web/remotes/template src/web/remotes/new_web_app
##### pnpm install
#####
##### go to project root
##### cd ../.. 
#####
##### run
##### ./run_dev.sh



########################
# TODO
# go to OpenSchema root dir
# pnpm install

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
#docker compose --env-file .env.dev -f docker-compose-infra.yml build
#check_error
#docker compose --env-file .env.dev -f docker-compose-infra.yml down
#docker compose --env-file .env.dev -f docker-compose-infra.yml up -d

#####DOCKER_BUILDKIT=0 
#docker compose --env-file .env.dev -f docker-compose-service.yml build # --progress=plain # --no-cache
#check_error
#docker compose --env-file .env.dev -f docker-compose-service.yml down
#docker compose --env-file .env.dev -f docker-compose-service.yml up -d

#####DOCKER_BUILDKIT=0 
docker compose --env-file .env.dev -f docker-compose-web.yml build # --progress=plain # --no-cache
check_error
docker compose --env-file .env.dev -f docker-compose-web.yml down
docker compose --env-file .env.dev -f docker-compose-web.yml up -d