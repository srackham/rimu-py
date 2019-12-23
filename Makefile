# rimu-py Makefile

# Set defaults (see http://clarkgrubb.com/makefile-style-guide#prologue)
MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := test
.DELETE_ON_ERROR:
.SUFFIXES:
.ONESHELL:
# .SILENT:

# VERS is set to version number extracted from setup.py
VERS := $$(sed -ne 's/\s*version="\([0-9.]*\)",.*/\1/p' setup.py)
SRC_DIST := dist/rimu-$(VERS).tar.gz
BIN_DIST := dist/rimu-$(VERS)-py3-none-any.whl

.PHONY: test
test:
	PYTHONPATH=./src pytest tests/

.PHONY: build
# Build binary and source distributions.
build: test
	pip3 freeze > requirements.txt
	python3 setup.py sdist bdist_wheel

.PHONY: init
# Create virtual environment and install development dependencies.
init:
	if [ -d .venv ]; then
		echo "Virtual environment .venv directory already exists."
		exit 1
	fi
	python3 -m venv .venv
	source ./.venv/bin/activate
	pip3 install -r requirements.txt

.PHONY: clean
# Delete cache and intermediate files.
clean:
	rm -rf $$(find ./src -type d -name '*.egg-info' -o -name __pycache__)
	rm -rf ./build

.PHONY: install
# Install local binary distribution.
install:
	python3 -m pip install -v $(BIN_DIST)

.PHONY: uninstall
uninstall:
	python3 -m pip uninstall -y -v rimu

.PHONY: tag
tag:
	git tag -a -m "v$(VERS)" v$(VERS)

.PHONY: push
push:
	git push -u --tags origin master

.PHONY: publish
publish:
	twine upload --repository-url https://test.pypi.org/legacy/ $(SRC_DIST) $(BIN_DIST)