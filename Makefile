test:
	uv run pytest

doc:
	make -C docs clean doctest html SPHINXBUILD="uv run --group docs sphinx-build"
	open docs/_build/html/index.html
