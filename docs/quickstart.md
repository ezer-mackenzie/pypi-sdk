# Getting Started

## Requirements and installation

Python 3.11 or later is required. Install from this checkout:

```console
uv sync --group dev
```

After a package release, installation from PyPI will be:

```console
python -m pip install pypi-sdk
```

## Query project and release metadata

```python
from pypi_sdk import PypiClient

with PypiClient() as client:
    project = client.projects.get("sampleproject")
    release = client.projects.get_release("sampleproject", project.info.version)

    print(project.info.summary)
    for distribution in release.urls:
        print(distribution.filename, distribution.digests)
```

The client owns its HTTP connection pool. Use it as a context manager or call
`close()` when finished. Models preserve additional fields returned by PyPI.

## Query the Simple Index

```python
with PypiClient() as client:
    index = client.index.get_project("sampleproject")
    for file in index.files:
        print(file.filename, file.url, file.hashes)
```

Use the advertised digest to verify a downloaded file. The SDK returns metadata;
it does not download distributions.

## Read feeds and provenance

```python
with PypiClient() as client:
    recent = client.feeds.project_releases("sampleproject")
    provenance = client.integrity.get_provenance(
        "sampleproject",
        "4.0.0",
        "sampleproject-4.0.0.tar.gz",
    )
```

Provenance is only available for files with attestations. PyPI may return HTTP
404 when a file has no provenance.

## Errors

Catch `PypiError` for SDK failures and its subclasses for HTTP, protocol,
timeout, connection, and publishing errors. See [Errors](errors.md).
