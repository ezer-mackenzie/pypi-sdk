# Architecture

## Client and services

`PypiClient` owns one synchronous HTTPX connection pool and exposes narrow
services for the JSON API, the PEP 691 JSON Simple Index, PEP 740 provenance,
statistics, and RSS feeds. The context manager closes the pool. Service methods
return Pydantic response models that allow additive upstream fields.

## Publishing

`TwinePublisher` is independent of the read client. It validates local
distribution paths and invokes `python -m twine upload` without a shell. The
destination is explicit and authentication is scoped to the upload process.
Build and CI orchestration remain the responsibility of the package being
released.

## Deliberate boundaries

The SDK does not create undocumented account-management calls, custom package
builds, downloads, retries, or a second upload protocol. The RSS API is
available for polling; conditional ETag requests are not currently exposed.
The HTML representation of the Simple Index is not wrapped because PyPI
recommends JSON for new integrations.
