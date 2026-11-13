# PyPI SDK

An unofficial, typed Python SDK for PyPI's documented public APIs. It provides
one synchronous client for package metadata, the PEP 691 index, provenance,
statistics, RSS feeds, and a Twine-backed distribution publisher.

The SDK requires Python 3.11 or later. It is not affiliated with or endorsed by
the Python Software Foundation or the PyPI maintainers.

## What this SDK covers

| PyPI feature | SDK interface |
| --- | --- |
| Project and release JSON | `client.projects.get()` / `get_release()` |
| PEP 691 JSON Simple Index | `client.index.list_projects()` / `get_project()` |
| PEP 740 file provenance | `client.integrity.get_provenance()` |
| Package storage statistics | `client.stats.get()` |
| New package and release RSS feeds | `client.feeds` |
| Legacy upload endpoint | `client.publisher.upload()` via Twine |

It intentionally does not wrap the deprecated XML-RPC API, the partner-only
secret reporting API, or Google BigQuery datasets as if they were normal PyPI
HTTP endpoints. PyPI also does not provide a public general-purpose REST API to
manage accounts, collaborators, or edit an existing release. Add a new version
to publish an update; an existing release cannot be overwritten.

## Installation

Python 3.11 or later is required. From this checkout:

```console
uv sync --group dev --group docs
```

After publishing, install the SDK from PyPI:

```console
python -m pip install pypi-sdk
```

For uploads, install the optional Twine dependency:

```console
python -m pip install "pypi-sdk[publish]"
```

## Quick start

```python
from pypi_sdk import PypiClient

with PypiClient() as client:
    project = client.projects.get("sampleproject")
    release = client.projects.get_release("sampleproject", project.info.version)
    files = client.index.get_project("sampleproject").files
    print(project.info.summary, len(files), len(release.urls))
```

Responses are Pydantic models that preserve additional fields returned by PyPI.
The client uses anonymous GET requests by default, follows no redirects, and
does not retry automatically.

## Publish built distributions

Build and validate artifacts with the standard Python packaging tools, then
explicitly choose TestPyPI or PyPI. TestPyPI is a separate service, useful for
testing the release process before publishing to production.

```python
from pathlib import Path

from pypi_sdk import PypiClient

artifacts = Path("dist").glob("*")
with PypiClient() as client:
    result = client.publisher.upload(artifacts, repository="testpypi")
print(result.files)
```

Twine reads `TWINE_USERNAME` and `TWINE_PASSWORD` from the environment, or can
receive a token explicitly without placing it in process arguments:

```python
import os
from pathlib import Path

from pypi_sdk import PypiClient

token = os.environ["PYPI_API_TOKEN"]
with PypiClient() as client:
    client.publisher.upload(
        Path("dist").glob("*"),
        repository="pypi",
        token=token,
    )
```

The equivalent CLI command is:

```console
pypi-sdk upload --repository testpypi dist\your_package-1.0.0-py3-none-any.whl
```

The publisher delegates metadata handling and the upload protocol to Twine.
It does not build distributions; use `python -m build` or your project's
existing build backend first.

## Automated publishing with Trusted Publishing

For CI, prefer PyPI Trusted Publishing over long-lived API tokens. Configure
the GitHub repository and workflow as a trusted publisher in the PyPI project
settings using the GitHub repository owner, repository name, `publish.yml`, and
the `pypi` environment. Configure the matching GitHub Environment (add
protection rules if desired), then copy
[`examples/publish.yml`](examples/publish.yml) to
`.github/workflows/publish.yml` in the package being released. The workflow
builds and validates distributions, then publishes them through PyPI's official
GitHub Action using OIDC.
See the [Trusted Publishing guide](https://docs.pypi.org/trusted-publishers/).

## API policies and boundaries

- The SDK identifies itself with a `User-Agent` and honors PyPI's JSON
  representations. The Simple Index HTML representation is not wrapped; the
  docs recommend its JSON form for new integrations.
- If polling for updates, prefer RSS feeds and avoid bursts of thousands of
  requests. The current client does not yet expose conditional ETag requests.
- Use the Simple Index for distribution files and verify their advertised
  hashes after downloading.
- File upload creates releases one file at a time. The first file for a
  version creates that release and fixes its metadata. To correct a release,
  publish a new version.
- Project administration and Trusted Publisher setup happen in PyPI's web
  interface; this SDK does not claim unsupported account-management endpoints.

See the [PyPI API documentation](https://docs.pypi.org/api/) and the
[Python Packaging User Guide](https://packaging.python.org/).

## Development

```console
uv sync --group dev --group docs
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run basedpyright
uv run pytest
uv run --group docs mkdocs build --strict
uv build
```

Tests use mocked HTTP and do not upload packages or contact PyPI. Optional CPU
benchmarks are available with pytest-benchmark:

```console
uv run --group benchmark pytest benchmarks --no-cov --benchmark-only
```

BenchCore measurements require Python 3.12 or later:

```console
uv run --group benchcore pytest benchmarks/benchcore_cases.py --no-cov --benchcore-save=.benchcore
```

See [Getting started](docs/quickstart.md), [API reference](docs/api.md),
[publishing guide](docs/publishing.md), [development guide](docs/development.md),
[contributing](CONTRIBUTING.md), and the [changelog](CHANGELOG.md).
