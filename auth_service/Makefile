DOCKER_COMPOSE = docker-compose
DB_SERVICE = auth-db
SERVICE = auth-service
PYTHON = python3


.PHONY: makemigration migrate downgrade build up down


makemigration:
	$(DOCKER_COMPOSE) exec $(SERVICE) alembic revision --autogenerate -m "$(message)"

migrate:
	$(DOCKER_COMPOSE) exec $(SERVICE) alembic upgrade head

downgrade:
	$(DOCKER_COMPOSE) exec $(SERVICE) alembic downgrade $(revision)

build:
	$(DOCKER_COMPOSE) up --build

up:
	$(DOCKER_COMPOSE) up

down:
	$(DOCKER_COMPOSE) down
