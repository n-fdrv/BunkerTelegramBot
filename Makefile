.SILENT:

COLOR_RESET = \033[0m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m
COLOR_WHITE = \033[00m

.DEFAULT_GOAL := help


.PHONY: help
help:  # Вызвать help
	@echo -e "$(COLOR_GREEN)Makefile help:"
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "$(COLOR_GREEN)-$$(echo $$l | cut -f 1 -d':'):$(COLOR_WHITE)$$(echo $$l | cut -f 2- -d'#')\n"; done

start-db: # Запуск контейнера Postgres
	docker-compose -f infra/dev/docker-compose.local.yaml up -d; \
	if [ $$? -ne 0 ]; \
    then \
        docker compose -f infra/dev/docker-compose.local.yaml up -d; \
		docker compose version; \
    fi

stop-db: # Остановка контейнера Postgres
	docker-compose -f infra/dev/docker-compose.local.yaml down; \
	if [ $$? -ne 0 ]; \
    then \
		docker compose -f infra/dev/docker-compose.local.yaml down; \
	fi

clear-db: # Очистка БД Postgres
	docker-compose -f infra/dev/docker-compose.local.yaml down --volumes; \
	if [ $$? -ne 0 ]; \
    then \
		docker compose -f infra/dev/docker-compose.local.yaml down --volumes; \
	fi

migrate: # Выполнение миграций Django
	poetry run python src/manage.py migrate

collectstatic: # Собрать статику Django
	poetry run python src/manage.py collectstatic --noinput

createsuperuser: # Создать супер пользователя
	poetry run python src/manage.py createsuperuser --noinput

upload-data: # Загрузить данные
	cd src && poetry run python manage.py upload_carts && cd ..

run-app: # Запуск Django и Telegram бота
	@echo -e "$(COLOR_YELLOW)Starting bot...$(COLOR_RESET)"
	@cd src && poetry run uvicorn core.asgi:application --reload && cd .. && \
	echo -e "$(COLOR_GREEN)Bot stopped$(COLOR_RESET)"

bot-init: # Базовая команда для запуска БД, миграций, бота и джанго
	make clear-db start-db migrate collectstatic createsuperuser upload-data run-app

bot-existing-bd: # запуск бота и контейнера PostgreSQL с существующими данными в БД:
	make start-db run-app
