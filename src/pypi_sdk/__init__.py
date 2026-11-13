"""Unofficial typed SDK for PyPI's documented public APIs."""

from pypi_sdk.client import PypiClient
from pypi_sdk.config import ClientConfig
from pypi_sdk.constants import SDK_VERSION
from pypi_sdk.errors import (
    PypiAuthenticationError,
    PypiAuthorizationError,
    PypiConnectionError,
    PypiError,
    PypiHTTPError,
    PypiNotFoundError,
    PypiProtocolError,
    PypiPublishError,
    PypiRateLimitError,
    PypiTimeoutError,
)
from pypi_sdk.models import (
    DistributionFile,
    FeedEntry,
    FeedResponse,
    ProjectInfo,
    ProjectResponse,
    ProvenanceResponse,
    SimpleProject,
    SimpleProjectResponse,
    SimpleProjectsResponse,
    StatsResponse,
)
from pypi_sdk.publish import Repository, TwinePublisher, UploadResult

__version__: str = SDK_VERSION

__all__ = [
    "ClientConfig",
    "DistributionFile",
    "FeedEntry",
    "FeedResponse",
    "ProjectInfo",
    "ProjectResponse",
    "ProvenanceResponse",
    "PypiAuthenticationError",
    "PypiAuthorizationError",
    "PypiClient",
    "PypiConnectionError",
    "PypiError",
    "PypiHTTPError",
    "PypiNotFoundError",
    "PypiProtocolError",
    "PypiPublishError",
    "PypiRateLimitError",
    "PypiTimeoutError",
    "Repository",
    "SDK_VERSION",
    "SimpleProject",
    "SimpleProjectResponse",
    "SimpleProjectsResponse",
    "StatsResponse",
    "TwinePublisher",
    "UploadResult",
    "__version__",
]
