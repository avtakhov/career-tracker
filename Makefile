install:
	pip3 install poetry && \
	poetry install

run:
	docker compose build && \
	docker compose up

build:
	docker compose build

up:
	docker compose up

migrate:
	docker compose run app alembic -c /app/app/core/db/alembic.ini upgrade head

downgrade:
	docker compose run app alembic -c /app/app/core/db/alembic.ini downgrade base

migration_file:
	docker compose run app alembic -c /app/app/core/db/alembic.ini revision --autogenerate
