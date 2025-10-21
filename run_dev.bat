docker compose --env-file .env.dev -f docker-compose-web.yaml down
docker compose --env-file .env.dev -f docker-compose-web.yaml build --no-cache
docker compose --env-file .env.dev -f docker-compose-web.yaml up -d

docker compose --env-file .env.dev -f docker-compose-web-template.yaml down
docker compose --env-file .env.dev -f docker-compose-web-template.yaml build --no-cache
docker compose --env-file .env.dev -f docker-compose-web-template.yaml up -d