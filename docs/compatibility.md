# Compatibility and Limitations

## Runtime support

- Python 3.11 and later.
- Pydantic 2.x response models.
- HTTPX synchronous client.
- Twine is optional and is installed through the `publish` extra.
- BenchCore measurements require Python 3.12 or later.

CI checks the supported Python versions configured in `.github/workflows/ci.yml`.

## API coverage

The SDK wraps the PyPI project/release JSON API, PEP 691 JSON Simple Index,
PEP 740 Integrity API, storage stats, RSS feeds, and file upload through Twine.
It does not wrap Simple Index HTML, deprecated XML-RPC, or the partner-only
secret reporting API. BigQuery datasets use Google's BigQuery service rather
than a PyPI HTTP endpoint.

There is no public general-purpose REST API for account settings, project
collaborators, yanking, or editing uploaded releases. Use the PyPI web interface
where applicable.

## Caching and request policy

PyPI recommends a descriptive `User-Agent`, RSS for update polling, conditional
requests with ETags, serial request patterns, and mirrors for high-volume
downloads. This release identifies itself with a `User-Agent` and does not
implement an ETag cache or automatic retries. Callers should avoid request
bursts and cache responses when appropriate.
