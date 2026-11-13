"""Typed access to PyPI's documented public read APIs."""

from collections.abc import Callable
from typing import TypeVar
from urllib.parse import quote
from xml.etree import ElementTree

from pydantic import BaseModel, ValidationError

from pypi_sdk.errors import PypiProtocolError
from pypi_sdk.models import (
    FeedEntry,
    FeedResponse,
    ProjectResponse,
    ProvenanceResponse,
    SimpleProjectResponse,
    SimpleProjectsResponse,
    StatsResponse,
)

ModelT = TypeVar("ModelT", bound=BaseModel)


class ProjectService:
    """PyPI JSON API project and release metadata."""

    def __init__(self, get_json: Callable[[str, str], ProjectResponse]) -> None:
        self._get_json = get_json

    def get(self, name: str) -> ProjectResponse:
        """Get the project metadata and release file list."""
        return self._get_json(f"/pypi/{quote(_identifier(name), safe='')}/json", "application/json")

    def get_release(self, name: str, version: str) -> ProjectResponse:
        """Get metadata for one release."""
        path = (
            f"/pypi/{quote(_identifier(name), safe='')}/{quote(_identifier(version), safe='')}/json"
        )
        return self._get_json(path, "application/json")


class IndexService:
    """PEP 691 JSON Simple Repository API."""

    def __init__(
        self,
        get_projects: Callable[[str, str], SimpleProjectsResponse],
        get_project: Callable[[str, str], SimpleProjectResponse],
    ) -> None:
        self._get_projects = get_projects
        self._get_project = get_project

    def list_projects(self) -> SimpleProjectsResponse:
        """List registered projects from the Simple Index."""
        return self._get_projects("/simple/", "application/vnd.pypi.simple.v1+json")

    def get_project(self, name: str) -> SimpleProjectResponse:
        """List available distributions for a project."""
        path = f"/simple/{quote(_identifier(name), safe='')}/"
        return self._get_project(path, "application/vnd.pypi.simple.v1+json")


class IntegrityService:
    """PEP 740 provenance lookup."""

    def __init__(self, get_json: Callable[[str, str], ProvenanceResponse]) -> None:
        self._get_json = get_json

    def get_provenance(self, project: str, version: str, filename: str) -> ProvenanceResponse:
        """Get attestations and publisher identity for a distribution."""
        path = (
            f"/integrity/{quote(_identifier(project), safe='')}/"
            f"{quote(_identifier(version), safe='')}/"
            f"{quote(_identifier(filename), safe='')}/provenance"
        )
        return self._get_json(path, "application/vnd.pypi.integrity.v1+json")


class StatsService:
    """Package storage statistics."""

    def __init__(self, get_json: Callable[[str, str], StatsResponse]) -> None:
        self._get_json = get_json

    def get(self) -> StatsResponse:
        """Get total PyPI package size and the top 100 packages by size."""
        return self._get_json("/stats/", "application/json")


class FeedService:
    """PyPI RSS feeds for package and release updates."""

    def __init__(self, get_text: Callable[[str, str], str]) -> None:
        self._get_text = get_text

    def new_packages(self) -> FeedResponse:
        """Get the newest projects feed."""
        return self._parse(self._get_text("/rss/packages.xml", "application/rss+xml"))

    def latest_updates(self) -> FeedResponse:
        """Get the latest project releases feed."""
        return self._parse(self._get_text("/rss/updates.xml", "application/rss+xml"))

    def project_releases(self, name: str) -> FeedResponse:
        """Get recent releases for a project."""
        path = f"/rss/project/{quote(_identifier(name), safe='')}/releases.xml"
        return self._parse(self._get_text(path, "application/rss+xml"))

    @staticmethod
    def _parse(xml: str) -> FeedResponse:
        try:
            root = ElementTree.fromstring(xml)
            channel = root.find("channel")
            if channel is None:
                raise ValueError("missing RSS channel")
            entries = [
                FeedEntry.model_validate(
                    {
                        child.tag: child.text
                        for child in item
                        if child.tag
                        in {"title", "link", "description", "pubDate", "guid", "category"}
                    }
                )
                for item in channel.findall("item")
            ]
            return FeedResponse(title=channel.findtext("title"), entries=entries)
        except (ElementTree.ParseError, ValidationError, ValueError):
            raise PypiProtocolError("PyPI returned an invalid RSS feed") from None


def parse_model(model_type: type[ModelT], payload: object) -> ModelT:
    """Validate a documented response and hide payload data from error messages."""
    try:
        return model_type.model_validate(payload)
    except ValidationError:
        raise PypiProtocolError("PyPI returned an unexpected JSON response") from None


def _identifier(value: str) -> str:
    if not value or not value.strip():
        raise ValueError("path identifiers must not be empty")
    return value
