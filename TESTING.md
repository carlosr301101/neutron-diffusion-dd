# Testing with UV

This document explains how to run the unit tests for the neutron transport simulation project using UV.

## What is UV?

UV is an extremely fast Python package installer and resolver, written in Rust. It can be used as a drop-in replacement for pip and pip-tools, and includes additional functionality like a global command runner (uvx) and project management tools.

## Prerequisites

Make sure you have UV installed. If not, install it using:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

## Running Tests with UV

### Method 1: Using uvx (Recommended)

The easiest way to run tests is using `uvx`, which allows you to run commands from Python packages without installing them globally:

```bash
# Run all tests
uvx --with numpy,pandas,pytest pytest

# Run all tests with verbose output
uvx --with numpy,pandas,pytest pytest -v

# Run tests in a specific file
uvx --with numpy,pandas,pytest pytest test/test_config.py

# Run a specific test
uvx --with numpy,pandas,pytest pytest test/test_config.py::test_config_initialization

# Run tests with coverage
uvx --with numpy,pandas,pytest pytest --cov=src test/
```

### Method 2: Using UV to create a virtual environment

1. Create a new virtual environment:
```bash
uv venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv pip install pytest numpy pandas
```

3. Run the tests:
```bash
pytest
```

### Method 3: Using UV to sync dependencies from pyproject.toml

If you have a `pyproject.toml` file with test dependencies, you can:

1. Install all dependencies:
```bash
uv sync
```

2. Activate the environment:
```bash
source .venv/bin/activate
```

3. Run tests:
```bash
pytest
```

## Test Structure

The tests are organized in the `test/` directory:

- `test_config.py` - Tests for the Config class
- `test_runner.py` - Tests for the Runner class
- `test_cuadraturas.py` - Tests for the quadrature module
- `test_utils.py` - Tests for utility functions

## Common Test Commands

```bash
# Run all tests
uvx --with numpy,pandas,pytest pytest

# Run tests with detailed output
uvx --with numpy,pandas,pytest pytest -v

# Run tests matching a pattern
uvx --with numpy,pandas,pytest pytest -k "config"

# Run tests and show print statements
uvx --with numpy,pandas,pytest pytest -s

# Run tests in parallel (if pytest-xdist is available)
uvx --with numpy,pandas,pytest pytest -n auto

# Generate coverage report
uvx --with numpy,pandas,pytest pytest --cov=src --cov-report=html
```

## Troubleshooting

If you encounter issues:

1. Make sure your Python environment is clean
2. Verify that all dependencies are available
3. Check that the test files are in the correct location

```bash
# Check if pytest is available via uvx
uvx --with pytest pytest --version

# Install specific version of pytest if needed
uvx --with pytest==8.0.0 pytest --version
```

## Required Dependencies

The tests require the following Python packages:
- pytest
- numpy
- pandas

When using uvx, these can be specified with the `--with` flag as shown in the examples above.