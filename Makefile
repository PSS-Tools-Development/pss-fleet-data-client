.PHONY: all
all: format check test

# setup
.PHONY: init-dev
init-dev:
	rye self update
	rye sync --update-all
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
	pytest --cov=./src/api ./tests --cov-report xml:cov.xml

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
