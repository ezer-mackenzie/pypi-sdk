# Release Process

## Prepare a release

1. Select the next semantic version based on the actual public API change.
2. Update `pyproject.toml`, `src/pypi_sdk/constants.py`,
   `tests/test_api.py`, and `CHANGELOG.md` together.
3. Run all validation commands in `CONTRIBUTING.md`, including the strict docs
   build and package build.
4. Review the built wheel and source archive. Do not upload if the version,
   license, or package contents are inconsistent.
5. Commit the release preparation with a Conventional Commit message.
6. Create an annotated tag matching the package version, for example:

   ```console
   git tag -a v1.0.0 -m "Release v1.0.0"
   ```

7. Publish only after a repository remote and PyPI Trusted Publisher are
   configured. The release workflow uses the GitHub OIDC identity; it does not
   require a long-lived PyPI token. The configured publisher must match the
   repository owner, repository name, `publish.yml`, and the `pypi` environment.

Tags created in a local repository are local release markers until pushed to a
configured remote. Do not create placeholder tags or claim that a local tag has
been published to PyPI.
