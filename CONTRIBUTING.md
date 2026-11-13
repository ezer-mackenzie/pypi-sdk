# Contributing

Thanks for helping improve this unofficial PyPI SDK. Keep source code,
documentation, examples, and commit messages in English.

## Development setup

Install Python 3.11+ and uv, then create the locked development environment:

```console
uv sync --locked --group dev --group docs
```

Runtime dependencies belong in `[project.dependencies]`. Keep test, docs,
benchmark, and publishing tools in their corresponding optional groups. Update
`uv.lock` with uv; do not edit it by hand.

## Validation

Run the full offline checks before committing:

```console
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run basedpyright
uv run pytest
uv run --group docs mkdocs build --strict
uv build
```

Tests use HTTPX `MockTransport`; normal test runs do not contact PyPI or upload
files. Never test a write against production. Keep tests focused on observable
behavior and cover credential-sensitive code without real credentials.

Optional performance checks are opt-in:

```console
uv run --group benchmark pytest benchmarks --no-cov --benchmark-only
```

BenchCore requires Python 3.12+:

```console
uv run --group benchcore pytest benchmarks/benchcore_cases.py --no-cov --benchcore-save=.benchcore
```

Benchmark results are local artifacts and should not be committed.

## Changes and commits

Keep changes cohesive, preserve unrelated work, and use Conventional Commits,
for example:

```text
feat(api): add release metadata lookup
fix(publish): reject missing distributions
docs(publishing): explain Trusted Publishing
chore(release): prepare 1.0.0
```

Update the changelog and directly related docs for user-visible changes. Do not
create a version tag until the version in `pyproject.toml`, package constants,
and release notes agree and the validation above passes. Tags are release
markers, not placeholders for future versions.

Commits created by Copilot include this trailer:

```text
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

## Publishing

Use the repository release workflow and PyPI Trusted Publishing once a remote
and trusted publisher are configured. Do not put long-lived PyPI tokens in
workflow files or command-line arguments. Test releases on TestPyPI first.