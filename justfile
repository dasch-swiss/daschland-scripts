# List all recipes
default:
    @just --list


# Run all autoformattings
[no-exit-message]
format:
    ruff format .
    just ruff-check --fix


# Rebuild the virtual environment (must be run before `just lint`, otherwise several tools will try to do it in parallel)
[no-exit-message]
uv-sync:
    uv sync


# Run all linters in parallel (see https://just.systems/man/en/running-tasks-in-parallel.html)
[no-exit-message]
lint: uv-sync
    #!/usr/bin/env -S parallel --shebang --ungroup --jobs {{ num_cpus() }}
    just ruff-check
    just ruff-format-check
    just mypy


# Check Python files to detect bad coding habits
[no-exit-message]
ruff-check *FLAGS:
    uv run ruff check . {{FLAGS}}


# Check the formatting of the Python files
[no-exit-message]
ruff-format-check:
    uv run ruff format --check .


# Check type annotations
[no-exit-message]
mypy:
    uv run mypy . --exclude "src/excel2xml"


# Run the unit tests
[no-exit-message]
test *FLAGS:
    uv run pytest {{FLAGS}}


# Remove artifact files
[no-exit-message]
clean:
    -find . -name "*.pyc" -exec rm -rf {} +
    -find . -name __pycache__ -exec rm -rf {} +
    -find . -name .ruff_cache -exec rm -rf {} +
    -find . -name .pytest_cache -exec rm -rf {} +
    -find . -name .mypy_cache -exec rm -rf {} +
    -rm -rf ./*id2iri_mapping*.json
    -rm -rf ./*id2iri_[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]*.json
    -rm -f ./warnings.log
