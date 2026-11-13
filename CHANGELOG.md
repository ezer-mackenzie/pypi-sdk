# Changelog

User-visible changes are recorded here. This project follows semantic
versioning; compatibility changes are called out explicitly.

## 1.0.0

### Added

- Typed synchronous clients for PyPI project/release JSON, the PEP 691 JSON
  Simple Index, PEP 740 provenance, storage statistics, and RSS feeds.
- Optional Twine-backed publishing to PyPI or TestPyPI, plus a GitHub Actions
  Trusted Publishing example.
- Python 3.11+ support, strict BasedPyright and Mypy checks, coverage-enforced
  tests, pytest-benchmark, and optional BenchCore measurements.
- English API, publishing, development, compatibility, security, and release
  documentation.

### Changed

- Preserve the JSON and RSS fields returned by PyPI while typing stable fields.
- Keep account administration, the partner-only secret API, BigQuery, and
  deprecated XML-RPC outside the HTTP SDK surface.
