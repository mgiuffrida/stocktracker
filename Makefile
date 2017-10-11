all: test pep8 lint

source_pyfiles = stocktracker/*.py
test_pyfiles = tests/*.py
all_pyfiles = $(source_pyfiles) $(test_pyfiles)

init:
	pip install -r requirements.txt

test:
	python -m unittest discover

pep8:
	pep8 $(all_pyfiles)

lint:
	pylint --score=no $(source_pyfiles)
	pylint --score=no --rcfile=tests/.pylintrc $(test_pyfiles)

lint-quiet:
	pylint -E $(all_pyfiles)

clean:
	rm */*.pyc
