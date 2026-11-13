# API Reference

## Supported client

`PypiClient` is a synchronous context-managed client. Its service attributes
are:

| Service | Methods |
| --- | --- |
| `projects` | `get(name)`, `get_release(name, version)` |
| `index` | `list_projects()`, `get_project(name)` |
| `integrity` | `get_provenance(project, version, filename)` |
| `stats` | `get()` |
| `feeds` | `new_packages()`, `latest_updates()`, `project_releases(name)` |
| `publisher` | `upload(distributions, *, repository, token=None)` |

`publisher.upload` requires an explicit `repository` of `pypi` or `testpypi`.
It delegates to the optional Twine dependency and accepts built files; it does
not build distributions.

## Public exports

The package root exports the client, configuration, response models, publisher,
and SDK exception hierarchy:

::: pypi_sdk
    options:
      members:
        - ClientConfig
        - DistributionFile
        - FeedEntry
        - FeedResponse
        - ProjectInfo
        - ProjectResponse
        - ProvenanceResponse
        - PypiClient
        - PypiError
        - PypiHTTPError
        - PypiAuthenticationError
        - PypiAuthorizationError
        - PypiConnectionError
        - PypiNotFoundError
        - PypiProtocolError
        - PypiPublishError
        - PypiRateLimitError
        - PypiTimeoutError
        - SimpleProject
        - SimpleProjectResponse
        - SimpleProjectsResponse
        - StatsResponse
        - TwinePublisher
        - UploadResult
