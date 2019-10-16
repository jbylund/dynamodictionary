.PHONY: upload test

upload: lint increment_version test
	/bin/rm -rvf dynamodictionary.egg-info/ dist/ build/ prof/
	python setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	twine upload dist/*
	/bin/rm -rvf dynamodictionary.egg-info/ dist/ build/ prof/

increment_version: test
	true

test:
	PYTHONPATH=$(shell pwd)/src/dynamodict python -m pytest -s -vvv 

lint:
	autopep8 --in-place --aggressive --max-line-length 132 $(shell find . -name "*.py")
