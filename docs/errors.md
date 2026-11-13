# Errors

All SDK exceptions derive from `PypiError`.

| Exception | Meaning |
| --- | --- |
| `PypiHTTPError` | PyPI returned a non-success status; includes `status_code` and `endpoint` |
| `PypiAuthenticationError` | HTTP 401 |
| `PypiAuthorizationError` | HTTP 403 |
| `PypiNotFoundError` | HTTP 404 |
| `PypiRateLimitError` | HTTP 429; the SDK does not retry |
| `PypiConnectionError` | The HTTP request could not complete |
| `PypiTimeoutError` | The request timed out |
| `PypiProtocolError` | The response did not match the documented JSON or RSS format, or the client was closed |
| `PypiPublishError` | Twine returned a non-zero exit code; includes `exit_code` |

HTTP errors intentionally do not retain raw response bodies. This avoids
embedding arbitrary server data or credentials in exception strings. Twine's
own command output is inherited by the current process to preserve its
diagnostics.
