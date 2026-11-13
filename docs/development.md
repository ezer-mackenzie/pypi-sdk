# Development

## Setup and checks

```console
uv sync --locked --group dev --group docs
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run basedpyright
uv run pytest
uv run --group docs mkdocs build --strict
uv build
```

Pytest runs offline tests with branch coverage enabled. The `tests/` directory
is the default test target; opt-in benchmark modules are kept outside it.

## Optional benchmark groups

Install and run `pytest-benchmark` measurements:

```console
uv run --group benchmark pytest benchmarks --no-cov --benchmark-only
```

Install and run BenchCore on Python 3.12 or later:

```console
uv run --python 3.12 --group benchcore pytest benchmarks/benchcore_cases.py --no-cov --benchcore-save=.benchcore
```

Both benchmark suites validate large in-memory project and Simple Index
responses. They make no network requests and impose no timing thresholds.
Benchmark reports are local output and are ignored by Git.

## Dependency groups

`dev` contains test and static-analysis tools. `docs` contains MkDocs. `benchmark`
contains pytest-benchmark. `benchcore` contains the separate BenchCore pytest
integration and is restricted to Python 3.12+.
