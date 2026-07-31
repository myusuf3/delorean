test:
	uv run pytest

doc:
	make -C docs clean doctest html
	open docs/_build/html/index.html
