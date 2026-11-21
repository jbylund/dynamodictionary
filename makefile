.PHONY: test lint clean

# Releases are published by CI: bump the version in setup.py and src/dynamodict/__init__.py,
# and merge to main (see .github/workflows/ci.yml).

# Needs AWS credentials: the tests create and delete real DynamoDB tables.
test:
	python -m pytest -vvv --durations=5

lint:
	pre-commit run --all-files

clean:
	rm -rf build dist prof dynamodictionary.egg-info/ .pytest_cache
