test:
	uv run pytest

format:
	uv run black delorean tests docs/conf.py
	uv run ruff check --fix delorean tests docs/conf.py

lint:
	uv run black --check --diff delorean tests docs/conf.py
	uv run ruff check delorean tests docs/conf.py

doc:
	make -C docs clean doctest html SPHINXBUILD="uv run --group docs sphinx-build"
	open docs/_build/html/index.html
