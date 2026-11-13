import json
import sys
from pathlib import Path

import httpx
import pytest

from pypi_sdk import PypiClient, UploadResult
from pypi_sdk.cli import main
from pypi_sdk.publish import Repository


@pytest.mark.parametrize(
    ("arguments", "expected_path"),
    [
        (["project", "demo"], "/pypi/demo/json"),
        (["release", "demo", "1.2.0"], "/pypi/demo/1.2.0/json"),
    ],
)
def test_cli_project_and_release_commands(
    arguments: list[str],
    expected_path: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == expected_path
        return httpx.Response(
            200,
            json={"info": {"name": "demo", "version": "1.2.0"}, "urls": []},
        )

    monkeypatch.setattr(sys, "argv", ["pypi-sdk", *arguments])
    monkeypatch.setattr(
        "pypi_sdk.cli.PypiClient",
        lambda: PypiClient(transport=httpx.MockTransport(handler)),
    )

    main()

    output = json.loads(capsys.readouterr().out)
    assert output["info"]["name"] == "demo"
    assert output["info"]["version"] == "1.2.0"


@pytest.mark.parametrize("repository", ["pypi", "testpypi"])
def test_cli_upload_selects_repository(
    repository: Repository, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    uploads: list[tuple[list[str], Repository]] = []

    class FakePublisher:
        def upload(self, distributions: list[str], *, repository: Repository) -> UploadResult:
            uploads.append((distributions, repository))
            return UploadResult(
                repository=repository,
                files=tuple(Path(distribution) for distribution in distributions),
            )

    monkeypatch.setattr(
        sys,
        "argv",
        ["pypi-sdk", "upload", "--repository", repository, "dist/demo.whl"],
    )
    monkeypatch.setattr("pypi_sdk.cli.TwinePublisher", FakePublisher)

    main()

    assert uploads == [(["dist/demo.whl"], repository)]
    assert capsys.readouterr().out == f"Uploaded 1 file(s) to {repository}.\n"
