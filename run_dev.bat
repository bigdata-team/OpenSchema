docker compose --env-file .env.dev -f docker-compose-ui.yaml down
docker compose --env-file .env.dev -f docker-compose-ui.yaml build --no-cache
docker compose --env-file .env.dev -f docker-compose-ui.yaml up -d
