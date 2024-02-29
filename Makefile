POETRY_PYTHON_PATH = $(shell poetry env info --path)
POETRY_PYTHON_PATH := $(subst  ,,$(POETRY_PYTHON_PATH))

ifeq ($(OS),Windows_NT)
	PYTHON = $(addsuffix \Scripts\python.exe,$(POETRY_PYTHON_PATH))
else
	PYTHON = $(addsuffix /bin/python,$(POETRY_PYTHON_PATH))
endif

ifeq (add,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

ifeq (remove,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

init:
	poetry install

run:
	$(PYTHON) -m bot

install-beautifier:
	@pip install black isort
	@echo "installed beautifiers."

beautiful:
	@isort .
	@black .
	@echo "beautified code."

add:
	@poetry add $(RUN_ARGS)
	@poetry export -f requirements.txt --output requirements.txt --without-hashes
	@echo "added module(s) $(RUN_ARGS)."

remove:
	@poetry remove $(RUN_ARGS)
	@poetry export -f requirements.txt --output requirements.txt --without-hashes
	@echo "removed module(s) $(RUN_ARGS)."

.PHONY: init run install-beautifier beautiful add remove
