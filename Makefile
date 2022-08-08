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

# VERS extracts the version number from setup.py
VERS := $$(sed -ne 's/\s*version="\([0-9]\+[.][0-9]\+[.][0-9]\+[ab][0-9]\+\)",.*/\1/p' setup.py)
SRC_DIST := dist/rimu-$(VERS).tar.gz
BIN_DIST := dist/rimu-$(VERS)-py3-none-any.whl
RESOURCE_FILES = src/rimuc/resources/*
RESOURCES_PY = src/rimuc/resources.py
PYTHONPATH = ./src

.PHONY: test
test: resources lint
	vers=$(VERS)
	if [ -z "$$vers" ]; then
		echo setup.py: illegal version number
		exit 1
	fi
	echo pytest...
	PYTHONPATH=$(PYTHONPATH) pytest --quiet tests

.PHONY: lint
# lint source code.
lint: resources
	echo pylint...
	pylint src tests
	echo mypy...
	mypy src tests

.PHONY: version
version:
	echo $(VERS)

.PHONY: repl
# Open Python REPL.
repl:
	PYTHONPATH=$(PYTHONPATH) python3

.PHONY: build
# Build binary and source distributions.
build: test
	if [ -f "$(BIN_DIST)" -a ! -w "$(BIN_DIST)" ]; then
		echo "build error: $(BIN_DIST) previously published: bump the version number"
		exit 1
	fi
	if ! grep "^VERSION = '$(VERS)'" src/rimuc/rimuc.py > /dev/null; then
		echo "rimuc.py: VERSION does not match setup.py version $(VERS)."
		exit 1
	fi
	python3 setup.py --quiet sdist bdist_wheel

.PHONY: resources
# Build resources file.
resources: $(RESOURCES_PY)

$(RESOURCES_PY): $(RESOURCE_FILES)
	# Build resources.py containing Map<filename,contents> of rimuc resource files.
	echo "Building resources $@"
	echo "# Generated automatically from resource files. Do not edit." > $@
	echo "from typing import Dict" >> $@
	echo "resources: Dict[str, str] = {" >> $@
	for f in $^; do
		echo -n "    '$$(basename $$f)': " >> $@
		echo "r'''$$(cat $$f)'''," >> $@
	done
	echo "}" >> $@

.PHONY: clean
# Delete cache and intermediate files.
clean:
	rm -rf $$(find ./src ./tests -type d -name '*.egg-info' -o -name __pycache__)
	rm -rf ./build/*
	rm -rf ./.pytest_cache/*
	rm -rf ./.mypy_cache/*

.PHONY: install
# Install local binary distribution.
install:
	python3 -m pip install --ignore-installed $(BIN_DIST)

.PHONY: uninstall
uninstall:
	python3 -m pip uninstall -y rimu

.PHONY: tag
tag: test
	tag=v$(VERS)
	echo tag: $$tag
	git tag -a -m $$tag $$tag

.PHONY: push
push: test
	git push -u --tags origin master

.PHONY: publish
# Publish to PyPI production site.
publish: build
	twine upload $(SRC_DIST) $(BIN_DIST)
	chmod 444 $(SRC_DIST) $(BIN_DIST)

.PHONY: publish-testpypi
# Publish package to PyPI test site https://test.pypi.org/
# See https://packaging.python.org/en/latest/guides/using-testpypi/
publish-testpypi: build
	twine upload --repository testpypi $(SRC_DIST) $(BIN_DIST)

.PHONY: install-testpypi
# Install package from PyPI test site https://test.pypi.org/
# See https://packaging.python.org/en/latest/guides/using-testpypi/
install-testpypi:
	python3 -m pip install --index-url https://test.pypi.org/simple/ --ignore-installed rimu