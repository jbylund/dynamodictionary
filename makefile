.PHONY: upload test

upload: lint increment_version test
	find ./dist/ -delete
	python setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	twine upload dist/*
	/bin/rm -rvf dynamodictionary.egg-info/ dist/ build/

increment_version: test
	true

test:
	PYTHONPATH=$(shell pwd)/src/dynamodict python -m pytest -vvv 

lint:
	autopep8 --in-place --aggressive --max-line-length 132 $(shell find . -name "*.py")
