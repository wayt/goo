#
# goo Makefile
#

LIBRARY_DIR=goo
VENV_DIR=venv
TESTS_DIR=tests
PYTHON_VERSION=3.6.1

PYTHON=${VENV_DIR}/bin/python
PIP=${VENV_DIR}/bin/pip
PEP8=${VENV_DIR}/bin/pep8

all: pep8 tests

pyenv:
	pyenv local 3.6.1

venv: pyenv
	if [ ! -d "${VENV_DIR}" ]; then python -m venv ${VENV_DIR}; fi

requirements: venv
	${PIP} install -r requirements.txt


pep8: requirements
	${PEP8} -v ${LIBRARY_DIR} --max-line-length=120

tests: pyenv venv requirements
	${PYTHON} -m unittest discover -s .

release:
	${PYTHON} setup.py sdist upload -r pypi

.PHONY: all pyenv venv requirements pep8 tests release
