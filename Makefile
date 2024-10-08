.PHONY: all
all: format check test

# setup
.PHONY: init-dev
init-dev:
	rye self update
	rye sync --no-lock
	pre-commit install
	pre-commit run --all-files

.PHONY: update
update:
	rye sync --update-all

# formatting and linting
.PHONY: check
check:
	flake8 ./src
	vulture

.PHONY: format
format:
	autoflake .
	isort .
	black .

# testing
.PHONY: coverage
coverage:
	pytest --cov=./src/pss_fleet_data --cov-report=xml:cov.xml --cov-report=term

.PHONY: test
test:
	pytest ./tests

# build & publish
.PHONY: build
build:
	rye build --clean

.PHONY: publish
publish:
	rye build --clean
	rye publish --yes
