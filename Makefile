VENV_NAME?=venv
LIB_SRC?=rabbitmqbaselibrary
SRC?=${LIB_SRC} test

ARGS?=

help: ## Print this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

HAS_GIT          := $(shell command -v git;)
HAS_DOCKER       := $(shell command -v docker;)
HAS_PYTHON       := $(shell command -v python3;)

PYTHON=${VENV_NAME}/bin/python3

vendor: ## Preflight checks.
ifndef HAS_GIT
	$(error You must install git)
endif
ifndef HAS_DOCKER
	$(error must install docker)
endif
ifndef HAS_PYTHON
	$(error must install python)
endif

.PHONY: bootstrap
bootstrap: vendor py-all ## Initialise all the required artifacts.

.PHONY: py-all
py-all: py-init py-deps py-activate ## Initialize py and load requirements the python.

.PHONY: py-init
py-init: ## Initialize py virtual environment (venv).
	if [ ! -e "${VENV_NAME}/bin/activate.py" ] ; then python3 -m venv ${VENV_NAME} ; fi

.PHONY: py-deps
py-deps: ## Install python requirements.
	. ${VENV_NAME}/bin/activate && ${VENV_NAME}/bin/pip install -U -r requirements.txt

.PHONY: py-activate
py-activate: ## Activate python venv.
	. ${VENV_NAME}/bin/activate

.PHONY: py-deactivate
py-deactivate: ## Deactivate python venv.
	. ${VENV_NAME}/bin/deactivate

.PHONY: py-rm
py-rm: py-clean ## Remove python venv.
	rm -rf venv

.PHONE: py-lint
py-lint: ## Check static syntax errors or type errors
	${VENV_NAME}/bin/flake8 ${SRC}
	${VENV_NAME}/bin/mypy ${SRC}

.PHONE: py-safety
py-safety: ## static code security checks, dependency scan
	${VENV_NAME}/bin/safety check
	${VENV_NAME}/bin/bandit -r ${SRC}

.PHONY: py-test
py-test: ## Run the pytest test suite.
	${VENV_NAME}/bin/coverage run --source ${LIB_SRC} -m pytest
	${VENV_NAME}/bin/coverage report

.PHONY: py-clean
py-clean: ## Remove artifacts before new build.
	rm -rf dist
	rm -rf build
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -f .coverage

.PHONY: py-build
py-build: 	## Build a tarball distribution file
	${VENV_NAME}/bin/python3 setup.py sdist --formats=gztar
	${VENV_NAME}/bin/python3 setup.py bdist_wheel

.PHONE: py-upload
py-upload:  ## Upload a wheel to PyPi
	${VENV_NAME}/bin/twine check dist/*
	${VENV_NAME}/bin/twine upload dist/* --config-file .pypirc --verbose

.PHONY: py-full-build
py-full-build: py-activate py-clean py-safety py-lint py-test py-build ## Clean, check, test, build but not upload.
