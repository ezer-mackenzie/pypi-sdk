# Roadmap

## Current supported surface

The release target is a typed synchronous client for the documented PyPI
project/release JSON API, PEP 691 JSON Simple Index, PEP 740 provenance, storage
statistics, RSS feeds, and Twine-backed uploads. Tests are offline by default;
Trusted Publishing is demonstrated through GitHub Actions.

## Possible follow-up work

These are ideas, not release commitments:

- Conditional ETag requests and opt-in caching.
- A typed vulnerability response model if PyPI stabilizes its response schema.
- Async clients after sync/async API parity can be tested and documented.
- Additional CI providers' Trusted Publishing examples.
- A separate CLI that scaffolds package-specific release workflows.

The SDK will not grow wrappers for undocumented account-management endpoints or
partner-only APIs.
