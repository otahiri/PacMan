all: run

run: 
	uv run python3 pac-man.py config.json

debug:
	uv run python3 -m pdb src/__main__.py

install:
	uv sync

lint: install
	uv run mypy -m src --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

	uv run flake8 src
lint-strict:
	uv run flake8 .  && mypy . --strict

clean:
	rm -rf .mypy_cache
	find . -name "__pycache__" -type d -exec rm -rf {} +
