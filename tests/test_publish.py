import subprocess
from pathlib import Path

import pytest

from pypi_sdk import PypiPublishError, TwinePublisher


def test_upload_uses_twine_and_keeps_token_out_of_arguments(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    artifact = tmp_path / "demo-1.0.0-py3-none-any.whl"
    artifact.write_bytes(b"wheel")
    calls = []

    def fake_run(
        command: list[str], *, env: dict[str, str], check: bool
    ) -> subprocess.CompletedProcess[bytes]:
        calls.append((command, env, check))
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr("pypi_sdk.publish.subprocess.run", fake_run)
    result = TwinePublisher().upload([artifact], repository="testpypi", token="pypi-example-secret")

    command, environment, check = calls[0]
    assert result.files == (artifact,)
    assert result.repository == "testpypi"
    assert "https://test.pypi.org/legacy/" in command
    assert str(artifact) in command
    assert "pypi-example-secret" not in command
    assert environment["TWINE_USERNAME"] == "__token__"
    assert environment["TWINE_PASSWORD"] == "pypi-example-secret"
    assert check is False


def test_upload_requires_existing_artifacts(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        TwinePublisher().upload(
            [tmp_path / "missing.whl"],
            repository="testpypi",
        )


def test_upload_requires_an_explicit_supported_repository() -> None:
    with pytest.raises(ValueError, match="repository"):
        TwinePublisher().upload([], repository="invalid")  # type: ignore[arg-type]


def test_nonzero_twine_exit_is_reported(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    artifact = tmp_path / "demo.whl"
    artifact.write_bytes(b"wheel")

    def fake_run(
        command: list[str], *, env: dict[str, str], check: bool
    ) -> subprocess.CompletedProcess[bytes]:
        return subprocess.CompletedProcess(command, 1)

    monkeypatch.setattr("pypi_sdk.publish.subprocess.run", fake_run)
    with pytest.raises(PypiPublishError) as error:
        TwinePublisher().upload([artifact], repository="testpypi")

    assert error.value.exit_code == 1
