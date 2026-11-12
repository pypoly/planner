set positional-arguments
set dotenv-load


[working-directory: 'src']
makemigrations:
    uv run python manage.py makemigrations



[working-directory: 'src']
migrate:
    uv run python manage.py migrate


[working-directory: 'src']
admin:
    uv run python manage.py createsuperuser

[working-directory: 'src']
test *ARGS:
    uv run python manage.py test -v 3 $@

build:
    docker compose build

up *ARGS:
    docker compose up $@

down:
    docker compose down

init_admin:
    docker compose exec web python manage.py createsuperuser