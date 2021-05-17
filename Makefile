##########################################################################
# This is the project's Makefile.
##########################################################################

##########################################################################
# VARIABLES
##########################################################################

HOME := $(shell echo ~)
ENV := ENV_FILE=env
ENV_TEST := env.test
PYTHON := venv/bin/python

##########################################################################
# MENU
##########################################################################

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

##########################################################################
# TEST
##########################################################################

.PHONY: test
test: ## run test suite
	$(ENV_TEST) $(PYTHON) -m unittest discover ./ddd

################################################################################
# RELEASE
################################################################################

.PHONY: build
build: ## build the python package
	python setup.py sdist bdist_wheel

.PHONY: clean
clean: ## clean the build
	python setup.py clean
	rm -rf build dist ddd_for_python.egg-info
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

.PHONY: upload-test
upload-test: ## upload package to testpypi repository
	twine upload --repository testpypi --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload: ## upload package to pypi repository
	twine upload --skip-existing dist/*
