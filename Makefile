# rimu-py Makefile

# Set defaults (see http://clarkgrubb.com/makefile-style-guide#prologue)
MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := test
.DELETE_ON_ERROR:
.SUFFIXES:
.ONESHELL:
.SILENT:


.PHONY: test
test:
	# TODO

.PHONY: build
build: test
	# Build binary and source distributions.
	pip3 freeze > requirements.txt
	python3 setup.py sdist bdist_wheel

.PHONY: init
init:
	# Create virtual environment and install development dependencies.
	if [ -d .venv ]; then
		echo "Virtual environment .venv directory already exists."
		exit 1
	fi
	python3 -m venv .venv
	source ./.venv/bin/activate
	pip3 install -r requirements.txt
	# python3 -m pip  install --upgrade setuptools wheel twine pylint

.PHONY: clean
clean:
	# Delete cache and intermediate files.
	rm -rf $$(find ./src -type d -name '*.egg-info' -o -name __pycache__)
	rm -rf ./build

.PHONY: install
install:
	# Install local binary distribution.
	# TODO: install latest verison (extract version from setup.py, see go-rimu Makefile for example).
	python3 -m pip install -v dist/rimu-0.0.1-py3-none-any.whl

.PHONY: uninstall
uninstall:
	# Uninstall distribution.
	python3 -m pip uninstall -y -v rimu

.PHONY: publish
publish:
	# TODO: install latest verison.
	# Publish to TestPyPI.
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: push
push:
	git push -u --tags origin master