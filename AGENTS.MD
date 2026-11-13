# Repository Instructions for Coding Agents

## Project

This repository builds `pypi-sdk`, an unofficial typed Python client for PyPI's
documented APIs. Python imports use `pypi_sdk`. Code, docs, examples, benchmark
names, and commit messages are in English; communicate with the user in their
preferred language.

## Boundaries

- Keep the client synchronous and use the shared HTTPX client.
- Model documented API responses with Pydantic v2, preserving additive fields.
- Do not add account-management endpoints PyPI does not document as public APIs.
- Do not wrap deprecated XML-RPC, partner-only secret reporting, or BigQuery as
  PyPI HTTP endpoints.
- Publishing uploads built artifacts through Twine. Do not rebuild its upload
  protocol or claim that an existing release can be overwritten.
- Keep credentials explicit, out of logs/arguments, and scoped to upload.
- Avoid automatic retries, redirects, or network access in normal tests.

## Validation

Use the workspace `.venv` and locked uv dependencies. Before committing, run:

```console
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run basedpyright
uv run pytest
uv run --group docs mkdocs build --strict
uv build
```

BenchCore is optional and requires Python 3.12+. Never commit benchmark output.
Read `CONTRIBUTING.md`, `SECURITY.md`, and the `docs/` pages for release and
security requirements. Preserve unrelated work and do not claim remote
publication when only local commits or tags exist.