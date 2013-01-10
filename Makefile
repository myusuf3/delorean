test:
	python tests/test_data.py

doc:
	make -C docs html
	open docs/_build/html/index.html
