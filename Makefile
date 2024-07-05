.PHONY: tests requirements sync format clean dashboard

# Default Python interpreter
PYTHON := python3

# Virtual environment directory
VENV := venv

# Activate the virtual environment
ACTIVATE := . $(VENV)/bin/activate

# Install dependencies
requirements:
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install pip-tools
	$(ACTIVATE) && pip-compile requirements.in

# Run tests and linting
tests:
	$(ACTIVATE) && ruff check --fix .
	$(ACTIVATE) && ruff format .
	$(ACTIVATE) && pytest

# Format code
format:
	@echo 'Formatting project'
	$(ACTIVATE) && ruff check --fix --show-fixes .
	$(ACTIVATE) && ruff format --line-length 120 .

# Sync dependencies
sync:
	$(ACTIVATE) && pip-sync requirements.txt

# Clean up compiled Python files and cache
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf $(VENV)

# Run dashboard
dashboard:
	$(ACTIVATE) && streamlit run personal_finance_dashboard/dashboard.py

# Development setup
dev-setup: requirements sync
