.PHONY: tests requirements sync

# Default Python interpreter
PYTHON := python3

# Virtual environment directory
VENV := venv

# Activate the virtual environment
ACTIVATE := . $(VENV)/bin/activate

# Install dependencies
requirements:
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install -r requirements.txt

# Run tests and ruff
tests:
	$(ACTIVATE) && ruff check --fix .
	$(ACTIVATE) && ruff format .
	$(ACTIVATE) && pytest

# Format code
format:
	@echo
	@echo 'Formatting side-project'
	$(ACTIVATE) && ruff check --fix .
	$(ACTIVATE) && ruff format --line-length 120 .
	@echo
	@echo

# Sync dependencies
sync:
	$(ACTIVATE) && cp requirements.txt requirements.in && \
	pip-compile --upgrade --output-file requirements.txt requirements.in && \
	rm requirements.in && \
	pip-sync requirements.txt

# Clean up compiled Python files and cache
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

dashboard:
	$(ACTIVATE) && cd personal_finance_dashboard && streamlit run dashboard.py