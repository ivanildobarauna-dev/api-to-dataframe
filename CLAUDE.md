# API-TO-DATAFRAME DEVELOPMENT GUIDE

## Build & Test Commands
- Setup: `poetry install`
- Run all tests: `poetry run pytest`
- Run single test: `poetry run pytest tests/test_file.py::test_function`
- Coverage: `poetry run coverage run -m pytest && poetry run coverage report`
- Lint: `poetry run pylint src/`
- Format: `poetry run black src/ tests/`

## Code Style Guidelines
- Use Python 3.9+ features
- Import order: stdlib → third-party → local
- Type hints required for function parameters and return values
- Follow black formatting (max line length 88)
- Variable naming: snake_case for variables/functions, PascalCase for classes
- Error handling: use try/except with specific exceptions, log errors
- Use f-strings for string formatting
- Test coverage target: 90%+
- Use dataclasses or typed dictionaries for structured data

## Architecture
- MVC-like pattern: controllers, models, utils
- Core functionality in models package
- Client interactions in controller package