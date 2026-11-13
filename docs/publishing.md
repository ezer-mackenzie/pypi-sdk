# Publishing Distributions

PyPI accepts release files through its legacy upload endpoint. This SDK delegates
metadata extraction and upload protocol handling to Twine instead of implementing
a second uploader.

## Build and test locally

Build distributions with the project's configured backend, then check them with
Twine:

```console
python -m build
python -m twine check dist\your_package-1.0.0-py3-none-any.whl
```

Install the optional publisher dependency with `python -m pip install
"pypi-sdk[publish]"`. Test on TestPyPI first:

```console
pypi-sdk upload --repository testpypi dist\your_package-1.0.0-py3-none-any.whl
```

The Python API is:

```python
from pathlib import Path
from pypi_sdk import PypiClient

with PypiClient() as client:
    result = client.publisher.upload(
        Path("dist").glob("*"),
        repository="testpypi",
    )
```

Choose `repository="pypi"` only when the release is ready for production.
Publishing creates a release one file at a time. PyPI does not let a publisher
overwrite an uploaded file or edit the first file's release metadata; publish a
new version to correct a release.

## API tokens

Prefer Trusted Publishing for CI. For local publishing, pass a project-scoped
token through `token=` or set Twine's `TWINE_USERNAME=__token__` and
`TWINE_PASSWORD` environment variables. The SDK places an explicitly provided
token in the child process environment, not its argument list. Do not print or
commit the token.

## Trusted Publishing for CI

Configure the repository and workflow identity as a Trusted Publisher on the
PyPI project. The example workflow in `examples/publish.yml` builds the package
and uses PyPI's official GitHub Action with short-lived OIDC authentication.
For this SDK's own release, `.github/workflows/publish.yml` uses the same
approach once the repository remote and PyPI publisher are configured.

Trusted Publishing setup is performed in the PyPI web interface; it is not an
account-management operation offered by this SDK.
