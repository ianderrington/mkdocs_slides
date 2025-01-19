.PHONY: install test lint format clean docs

install:
	poetry install

test:
	poetry run pytest

lint:
	poetry run black --check .
	poetry run isort --check-only .

format:
	poetry run black .
	poetry run isort .

clean:
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:
	poetry run mkdocs serve

build:
	poetry build

publish:
	poetry publish 