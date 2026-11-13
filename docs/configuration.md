# Configuration

Pass either an API URL or a `ClientConfig`; do not pass both.

```python
from pypi_sdk import ClientConfig, PypiClient

config = ClientConfig(
    api_url="https://pypi.org",
    user_agent="example-package-inspector/1.0 (maintainer@example.org)",
    timeout=15,
    max_connections=10,
)

with PypiClient(config=config) as client:
    project = client.projects.get("sampleproject")
```

`api_url` must be HTTPS and cannot contain credentials, a query, or a fragment.
The default is `https://pypi.org`. `timeout` is a positive number of seconds;
`max_connections` must be a positive integer.

Read requests are anonymous. The client does not read API tokens from the
environment, forward credentials, follow redirects, or retry requests. Upload
credentials belong to the separate publisher; see [Publishing](publishing.md).
