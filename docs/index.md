# PyPI SDK

An unofficial, typed Python SDK for the documented public APIs hosted by PyPI.
It offers one synchronous HTTPX client for package and release metadata, the
PEP 691 JSON Simple Index, PEP 740 provenance, storage statistics, and RSS feeds.
Publishing delegates to the standard Twine client.

## What it is for

- Inspect project metadata and published distributions from Python.
- Discover files and their advertised hashes through PyPI's recommended JSON
  APIs.
- Retrieve file provenance and recent package/release updates.
- Upload already-built distributions locally, or use Trusted Publishing from CI.

## What it does not do

PyPI does not expose a public general-purpose REST API for account settings,
collaborator management, or editing existing releases. Publish a new version to
update a package. Partner-only secret reporting, Google BigQuery datasets, and
deprecated XML-RPC are outside this HTTP SDK.

## Start here

Install the SDK from this checkout with `uv sync --group dev`, then follow
[Getting started](quickstart.md). For new CI publishing, use
[Trusted Publishing](publishing.md#trusted-publishing-for-ci).
