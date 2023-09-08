export DOCKER_DEFAULT_PLATFORM=linux/arm64/v8

up:
	docker compose -f docker-compose-local.yaml up -d

down:
	docker compose -f docker-compose-local.yaml down --remove-orphans