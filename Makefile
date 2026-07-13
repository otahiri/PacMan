all: run

run:
	uv run python3 -m src

install:
	uv sync
	uv run pip install mazegenerator-2.0.2-py3-none-any.whl

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores\
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	rm -rf __pycache__ .mypy_cache
