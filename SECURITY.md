# Security Policy

## Supported versions

Security fixes target the latest supported release. Before a stable release,
the project has no older supported release lines or service-level guarantees.

## Reporting a vulnerability

Report suspected vulnerabilities privately to
ramirez.ruiz.eliezer@gmail.com. Include the affected version, impact,
and a minimal reproduction using synthetic credentials. Do not publish tokens,
personal data, or exploit details in public issues. No response-time commitment
is currently offered.

## Publishing credentials

Prefer PyPI Trusted Publishing in CI. For local publishing, use a project-scoped
API token and pass it through the SDK's `token` parameter or Twine's
`TWINE_PASSWORD` environment variable. Never commit tokens, print them, or place
them in command-line arguments. Revoke exposed tokens in PyPI; deleting a token
from a later commit does not revoke it.

The SDK keeps upload credentials out of read requests and subprocess arguments.
It cannot protect secrets that an application logs or passes to unrelated
processes. Uploading is an external side effect; use TestPyPI to validate a
workflow before production.