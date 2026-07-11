.PHONY: all
all: format check test


# setup
.PHONY: init-dev
init-dev:
	uv self update
	uv sync
	pre-commit install
	pre-commit run --all-files

.PHONY: update
update:
	uv sync --upgrade


# formatting and linting
.PHONY: check
check:
	uv run --no-project ruff check ./src
	uv run --no-project vulture ./src

.PHONY: format
format:
	uv run --no-project ruff check --fix ./src ./tests
	uv run --no-project ruff format ./src ./tests


# dev tools
.PHONY: lock
lock:
	uv export --no-hashes --no-header --no-annotate --no-dev --format requirements.txt > requirements.txt
	uv export --no-hashes --no-header --no-annotate --format requirements.txt > requirements-dev.txt


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
	uv build --clear

.PHONY: publish
publish:
	$(MAKE) build
	uv publish
