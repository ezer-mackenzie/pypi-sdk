# Claude Repository Guide

Read and follow [AGENTS.MD](AGENTS.MD), the canonical repository instructions.
Keep shared project rules there so this guide does not drift.

The distribution is `pypi-sdk`; the import package is `pypi_sdk`. This is an
unofficial synchronous client for PyPI's documented public APIs. The supported
surface and release boundaries are documented in `docs/api.md` and
`docs/compatibility.md`.

Use the workspace `.venv` and locked uv dependencies. Run the validation commands
from `AGENTS.MD`. Optional BenchCore runs only on Python 3.12+. Keep source,
documentation, and commit messages in English; answer the user in their preferred
language. Report only checks and releases actually completed.