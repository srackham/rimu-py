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


.PHONY: build
build:
	# Build binary and source distributions.
	python3 setup.py sdist bdist_wheel

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