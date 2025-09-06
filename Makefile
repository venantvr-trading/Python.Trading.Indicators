.PHONY: help install install-dev test test-coverage lint format clean build upload docs serve-docs
.DEFAULT_GOAL := help

PYTHON := python3
PIP := pip3
PACKAGE_NAME := venantvr
TEST_DIR := tests
DOCS_DIR := docs

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	$(PIP) install .

install-dev: ## Install package in development mode with dev dependencies
	$(PIP) install -e .
	$(PIP) install pytest pytest-cov black flake8 mypy sphinx sphinx-rtd-theme

test: ## Run tests
	$(PYTHON) -m pytest $(TEST_DIR) -v

test-coverage: ## Run tests with coverage report
	$(PYTHON) -m pytest $(TEST_DIR) --cov=$(PACKAGE_NAME) --cov-report=term-missing --cov-report=html

lint: ## Run linting checks
	$(PYTHON) -m flake8 $(PACKAGE_NAME) $(TEST_DIR)
	$(PYTHON) -m mypy $(PACKAGE_NAME)

format: ## Format code with black
	$(PYTHON) -m black $(PACKAGE_NAME) $(TEST_DIR)

format-check: ## Check code formatting without making changes
	$(PYTHON) -m black --check $(PACKAGE_NAME) $(TEST_DIR)

clean: ## Clean up build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: ## Build distribution packages
	$(PYTHON) -m build

upload: clean build ## Upload package to PyPI
	$(PYTHON) -m twine upload dist/*

upload-test: clean build ## Upload package to TestPyPI
	$(PYTHON) -m twine upload --repository testpypi dist/*

docs: ## Generate documentation
	cd $(DOCS_DIR) && $(PYTHON) -m sphinx -b html . _build/html

serve-docs: docs ## Serve documentation locally
	cd $(DOCS_DIR)/_build/html && $(PYTHON) -m http.server 8000

check: lint test ## Run all checks (linting and tests)

setup-dev: install-dev ## Setup development environment
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify everything is working."

release-check: format-check lint test-coverage ## Run all pre-release checks
	@echo "All checks passed! Ready for release."

# Development workflow targets
dev-test: ## Run tests in watch mode for development
	$(PYTHON) -m pytest $(TEST_DIR) -v --tb=short -x

quick-test: ## Run quick tests (no coverage)
	$(PYTHON) -m pytest $(TEST_DIR) -x --tb=line

# Quality gates
quality-gate: format-check lint test-coverage ## Full quality gate for CI/CD
	@echo "Quality gate passed!"