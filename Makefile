DOCKER_COMPOSE = docker-compose
DB_SERVICE = learning-db
SERVICE = learning-backend
PYTHON = python3


.PHONY: format build up down makemigration migrate downgrade right lint


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


format:
	isort .
	black .
	flake8 .

right:
	pyright .
	mypy .

lint:
	ruff check .
	ruff format .
	ruff check --fix .
	ruff format --fix .
	ruff check --fix .
