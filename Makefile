all: run

run: 
	uv run python3 -m src

install:
	uv sync

lint: install
	uv run mypy -m src --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

	uv run flake8 src

clean:
	rm -rf .mypy_cache
	find . -name "__pycache__" -type d -exec rm -rf {} +
