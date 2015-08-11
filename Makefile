test:
	nosetests --with-coverage --cover-package=delorean

doc:
	make -C docs html
	open docs/_build/html/index.html
