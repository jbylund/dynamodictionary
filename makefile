.PHONY: upload test

upload: increment_version test
	python setup.py sdist upload -r pypi

increment_version: test
	true

test:
	PYTHONPATH=$(shell pwd)/src/dynamodict python -m pytest -vvv 

lint:
	autopep8 --in-place --aggressive --max-line-length 132 $(shell find . -name "*.py")
