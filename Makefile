PROJECT_NAME=text-similarity
PYCMD=python3.7
PIPCMD=pip3.7
PIP_SOURCE=-i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
ENV_PATH=venv
PIP_INSTALL=$(PIPCMD) install $(PIP_SOURCE)
ROOT_PACKAGE=text-similarity

.PHONY: help env deps prod_deps lint lint_fix test test_file

help: Makefile
	@echo
	@echo " Choose a command to run in "$(PROJECT_NAME)":"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'

## env: Create a virtualenv
env:
	virtualenv -p $(PYCMD) $(ENV_PATH)

## deps: Install all the dependencies
deps:
	@cp .hooks/* .git/hooks/
	@if [ -z $(VIRTUAL_ENV) ]; then \
		echo 'You should source your virtualenv first by "source $(ENV_PATH)/bin/activate"'; \
	else \
		$(PIP_INSTALL) -r requirements.txt --use-deprecated=legacy-resolver; \
	fi

## update_deps: Use when updated requrements.txt
update_deps:
	$(PIPCMD) install -r requirements.txt --use-deprecated=legacy-resolver -U

## run: run a specific module. Runs `make run mod=crawlds`
run:
	@$(PYCMD) -m cmd.$(mod)

## lint: Run pylint on all project files
lint:
	@find . -name "*.py" -not -path "./$(ENV_PATH)/*" -not -path "./tests/*" | xargs flake8
