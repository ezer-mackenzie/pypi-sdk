"""Opt-in CPU benchmarks for PyPI response model validation."""

from pytest_benchmark.fixture import BenchmarkFixture

from pypi_sdk.models import ProjectResponse, SimpleProjectResponse


def _distribution(index: int) -> dict[str, object]:
    return {
        "filename": f"sampleproject-1.0.0-py3-none-any-{index}.whl",
        "url": f"https://files.pythonhosted.org/packages/sample-{index}.whl",
        "hashes": {"sha256": f"{index:064x}"},
        "size": index + 100,
        "yanked": False,
    }


def test_validate_project_response_with_1000_files(benchmark: BenchmarkFixture) -> None:
    payload: dict[str, object] = {
        "info": {"name": "sampleproject", "version": "1.0.0", "summary": "Sample"},
        "last_serial": 123,
        "urls": [_distribution(index) for index in range(1000)],
    }
    result = benchmark(ProjectResponse.model_validate, payload)

    assert result.info.name == "sampleproject"
    assert len(result.urls) == 1000


def test_validate_simple_index_with_1000_files(benchmark: BenchmarkFixture) -> None:
    payload: dict[str, object] = {
        "meta": {"api-version": "1.4", "_last-serial": 123},
        "name": "sampleproject",
        "files": [_distribution(index) for index in range(1000)],
        "versions": ["1.0.0"],
        "project-status": {"status": "active"},
    }
    result = benchmark(SimpleProjectResponse.model_validate, payload)

    assert result.name == "sampleproject"
    assert len(result.files) == 1000
