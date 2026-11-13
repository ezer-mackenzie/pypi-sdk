"""Explicitly selected BenchCore measurements; excluded from normal test discovery."""

import pytest
from benchcore.core.models import BenchmarkConfig
from benchcore.integrations.pytest import BenchCoreFixture

from pypi_sdk.models import ProjectResponse, SimpleProjectResponse


def _distribution(index: int) -> dict[str, object]:
    return {
        "filename": f"sampleproject-1.0.0-py3-none-any-{index}.whl",
        "url": f"https://files.pythonhosted.org/packages/sample-{index}.whl",
        "hashes": {"sha256": f"{index:064x}"},
        "size": index + 100,
        "yanked": False,
    }


@pytest.mark.benchcore(
    name="validate-project-json[files=1000]",
    config=BenchmarkConfig(rounds=20, warmup_rounds=2, iterations=10),
)
def test_validate_project_response(benchcore: BenchCoreFixture) -> None:
    payload: dict[str, object] = {
        "info": {"name": "sampleproject", "version": "1.0.0", "summary": "Sample"},
        "last_serial": 123,
        "urls": [_distribution(index) for index in range(1000)],
    }
    result = benchcore(ProjectResponse.model_validate, payload)

    assert result.value.info.name == "sampleproject"
    assert len(result.value.urls) == 1000


@pytest.mark.benchcore(
    name="validate-simple-index[files=1000]",
    config=BenchmarkConfig(rounds=20, warmup_rounds=2, iterations=10),
)
def test_validate_simple_index(benchcore: BenchCoreFixture) -> None:
    payload: dict[str, object] = {
        "meta": {"api-version": "1.4", "_last-serial": 123},
        "name": "sampleproject",
        "files": [_distribution(index) for index in range(1000)],
        "versions": ["1.0.0"],
        "project-status": {"status": "active"},
    }
    result = benchcore(SimpleProjectResponse.model_validate, payload)

    assert result.value.name == "sampleproject"
    assert len(result.value.files) == 1000
