all: test pep8 lint-full-quiet

init:
	pip install -r requirements.txt

test:
	python -m unittest discover

lint:
	pylint -E stocktracker/*.py tests/*.py

pep8:
	pep8 stocktracker/*.py tests/*.py

lint-full:
	pylint stocktracker/*.py
	pylint --rcfile=tests/.pylintrc tests/*.py

lint-full-quiet:
	pylint --score=no stocktracker/*.py
	pylint --score=no --rcfile=tests/.pylintrc tests/*.py

clean:
	rm **/*.pyc
