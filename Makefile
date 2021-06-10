.DEFAULT_GOAL := help
PKG = spacetar
PKG_DIR = src

dist: ## Build source distribution
	python setup.py sdist bdist_wheel

# NOTE: -e installs in "Development Mode".
# See: https://packaging.python.org/tutorials/installing-packages/
install: ## Install the package in development mode
	pip install -e .

# NOTE: remove the .egg-info directory from src/.
uninstall: ## Uninstall the package
	pip uninstall ${PKG}
	rm -rf ${PKG_DIR}/${PKG}.egg-info

# GLORIOUS hack to autogenerate Makefile help
# This simply parses the double hashtags that follow each Makefile command
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Print this help message
	@echo "Makefile help for ${PKG}"
	@echo "===================================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean: ## Remove all python cache and build files
	rm -rf tmp
	rm -rf dist
	rm -rf build
	rm -rf .eggs
	rm -f .coverage
	rm -rf .pytest_cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

upload_test: ## Upload the distribution source to the TEST PyPI
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: ## Upload the distribution source to the REAL PyPI
	twine upload dist/*

lint: ## Blacken all files.
	nox -s lint

tests: ## Run the unit tests and print a coverage report
	nox -s tests

.PHONY: dist install uninstall help clean upload upload_test lint tests