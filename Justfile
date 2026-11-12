set positional-arguments

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

