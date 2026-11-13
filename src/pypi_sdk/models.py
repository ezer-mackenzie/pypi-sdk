"""Typed response models; unknown upstream fields are preserved."""

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field


class PypiModel(BaseModel):
    """Base response model tolerant of additive fields from PyPI."""

    model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow", populate_by_name=True)


class ProjectInfo(PypiModel):
    name: str
    version: str
    summary: str | None = None
    description: str | None = None
    requires_python: str | None = None
    project_urls: dict[str, str] | None = None


class DistributionFile(PypiModel):
    filename: str
    url: str
    size: int | None = None
    hashes: dict[str, str] | None = None
    digests: dict[str, str] | None = None
    packagetype: str | None = None
    python_version: str | None = None
    requires_python: str | None = None
    upload_time: str | None = None
    yanked: bool | None = None
    yanked_reason: str | None = None
    core_metadata: bool | dict[str, str] | None = Field(default=None, alias="core-metadata")
    data_dist_info_metadata: bool | dict[str, str] | None = Field(
        default=None, alias="data-dist-info-metadata"
    )


class ProjectResponse(PypiModel):
    info: ProjectInfo
    last_serial: int | None = None
    releases: dict[str, list[DistributionFile]] = Field(default_factory=dict)
    urls: list[DistributionFile] = Field(default_factory=list)
    vulnerabilities: list[dict[str, object]] = Field(default_factory=list)


class SimpleIndexMeta(PypiModel):
    api_version: str | None = Field(default=None, alias="api-version")
    last_serial: int | None = Field(default=None, alias="_last-serial")


class SimpleProject(PypiModel):
    name: str
    last_serial: int | None = Field(default=None, alias="_last-serial")


class SimpleProjectsResponse(PypiModel):
    meta: SimpleIndexMeta
    projects: list[SimpleProject | str]


class SimpleProjectResponse(PypiModel):
    meta: SimpleIndexMeta
    name: str
    files: list[DistributionFile]
    versions: list[str] = Field(default_factory=list)
    project_status: dict[str, str] | None = Field(default=None, alias="project-status")


class ProvenanceResponse(PypiModel):
    version: int
    attestation_bundles: list[dict[str, object]]


class PackageSize(PypiModel):
    size: int


class StatsResponse(PypiModel):
    total_packages_size: int
    top_packages: dict[str, PackageSize]


class FeedEntry(PypiModel):
    title: str | None = None
    link: str | None = None
    description: str | None = None
    pub_date: str | None = Field(default=None, alias="pubDate")
    guid: str | None = None
    category: str | None = None


class FeedResponse(PypiModel):
    title: str | None = None
    entries: list[FeedEntry]
