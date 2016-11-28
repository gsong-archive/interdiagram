.DEFAULT_GOAL := test

LOCAL_IN = requirements/local.in
LOCAL_TXT = requirements/local.txt


install-dev-requirements:
	## Install requirements for local development environment
	pip install -q pip-tools
	pip-sync requirements/*.txt
	pip install -e .


pip-compile:
	## Update requirements/*.txt with latest packages from requirements/*.in
	pip install -q pip-tools
	pip-compile -U requirements/app.in
	pip-compile -U requirements/dev.in
	pip-compile -U requirements/app.in requirements/test.in \
		-o requirements/test.txt
ifneq (, $(wildcard $(LOCAL_IN)))
	pip-compile -U $(LOCAL_IN)
endif


test: type-check
	py.test --cov=interdiagram


test-html-coverage-report: type-check
	py.test --cov=interdiagram --cov-report=html


test-html-coverage-report-open: test-html-coverage-report
	open htmlcov/index.html


type-check:
	mypy interdiagram
