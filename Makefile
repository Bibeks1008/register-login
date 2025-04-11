installdeps:
	python3 -m pip install poetry
	poetry install

createmigrations:
	poetry run python3 manage.py makemigrations

migrate:
	poetry run python3 manage.py migrate

dev:
	poetry run python3 manage.py runserver 0.0.0.0:8000
