import httpx
import pytest

from pypi_sdk import (
    ClientConfig,
    PypiAuthenticationError,
    PypiAuthorizationError,
    PypiClient,
    PypiConnectionError,
    PypiError,
    PypiHTTPError,
    PypiNotFoundError,
    PypiProtocolError,
    PypiRateLimitError,
    PypiTimeoutError,
    SimpleProject,
)


def test_documented_api_services_use_expected_routes_and_accept_headers() -> None:
    responses = {
        "/pypi/demo/json": (
            "application/json",
            {
                "info": {"name": "demo", "version": "1.2.0", "summary": "Example"},
                "last_serial": 12,
                "releases": {"1.2.0": []},
                "urls": [],
                "vulnerabilities": [],
            },
        ),
        "/pypi/demo/1.2.0/json": (
            "application/json",
            {"info": {"name": "demo", "version": "1.2.0"}, "urls": []},
        ),
        "/simple/": (
            "application/vnd.pypi.simple.v1+json",
            {"meta": {"api-version": "1.4", "_last-serial": 12}, "projects": [{"name": "demo"}]},
        ),
        "/simple/demo/": (
            "application/vnd.pypi.simple.v1+json",
            {
                "meta": {"api-version": "1.4"},
                "name": "demo",
                "files": [
                    {
                        "filename": "demo-1.2.0-py3-none-any.whl",
                        "url": "https://files.pythonhosted.org/demo.whl",
                        "hashes": {"sha256": "abc"},
                        "core-metadata": False,
                    }
                ],
                "versions": ["1.2.0"],
                "project-status": {"status": "active"},
            },
        ),
        "/integrity/demo/1.2.0/demo-1.2.0.whl/provenance": (
            "application/vnd.pypi.integrity.v1+json",
            {"version": 1, "attestation_bundles": []},
        ),
        "/stats/": (
            "application/json",
            {"total_packages_size": 100, "top_packages": {"demo": {"size": 20}}},
        ),
    }
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        accept, body = responses[request.url.path]
        assert request.headers["accept"] == accept
        assert request.headers["user-agent"] == "pypi-sdk/1.0.0"
        assert "authorization" not in request.headers
        return httpx.Response(200, json=body)

    with PypiClient(transport=httpx.MockTransport(handler)) as client:
        project = client.projects.get("demo")
        release = client.projects.get_release("demo", "1.2.0")
        projects = client.index.list_projects()
        index = client.index.get_project("demo")
        provenance = client.integrity.get_provenance("demo", "1.2.0", "demo-1.2.0.whl")
        stats = client.stats.get()

    assert project.info.summary == "Example"
    assert release.info.version == "1.2.0"
    assert isinstance(projects.projects[0], SimpleProject)
    assert projects.projects[0].name == "demo"
    assert index.files[0].hashes == {"sha256": "abc"}
    assert provenance.version == 1
    assert stats.top_packages["demo"].size == 20
    assert [request.url.path for request in requests] == list(responses)


def test_rss_feed_is_parsed_into_typed_entries() -> None:
    xml = """<?xml version="1.0"?>
    <rss version="2.0"><channel><title>Recent releases</title>
      <item><title>demo 1.2.0</title><link>https://pypi.org/project/demo/</link>
        <description>Release details</description><pubDate>Wed, 12 Nov 2026 10:00:00 GMT</pubDate>
      </item>
    </channel></rss>"""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/rss/project/demo/releases.xml"
        assert request.headers["accept"] == "application/rss+xml"
        return httpx.Response(200, text=xml)

    with PypiClient(transport=httpx.MockTransport(handler)) as client:
        feed = client.feeds.project_releases("demo")

    assert feed.title == "Recent releases"
    assert feed.entries[0].title == "demo 1.2.0"
    assert feed.entries[0].pub_date == "Wed, 12 Nov 2026 10:00:00 GMT"


@pytest.mark.parametrize(
    ("status_code", "exception"),
    [(404, PypiNotFoundError), (302, PypiHTTPError)],
)
def test_http_errors_are_not_followed_or_retried(
    status_code: int, exception: type[PypiHTTPError]
) -> None:
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(status_code, headers={"Location": "https://example.com"})

    with PypiClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(exception) as error:
            client.projects.get("missing")

    assert len(requests) == 1
    if status_code == 404:
        assert error.value.status_code == status_code


@pytest.mark.parametrize(
    ("status_code", "exception"),
    [
        (401, PypiAuthenticationError),
        (403, PypiAuthorizationError),
        (429, PypiRateLimitError),
    ],
)
def test_specific_http_errors_are_mapped(status_code: int, exception: type[PypiHTTPError]) -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code)

    with PypiClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(exception) as error:
            client.projects.get("demo")

    assert error.value.status_code == status_code


def test_invalid_json_is_reported_as_protocol_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="not json")

    with PypiClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(PypiProtocolError, match="invalid JSON"):
            client.projects.get("demo")


def test_unexpected_json_shape_is_reported_as_protocol_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"unexpected": "shape"})

    with PypiClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(PypiProtocolError, match="unexpected JSON"):
            client.projects.get("demo")


def test_connection_error_is_reported_without_transport_details() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("private transport detail", request=request)

    with PypiClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(PypiConnectionError) as error:
            client.projects.get("demo")

    assert "private transport detail" not in str(error.value)


def test_timeout_is_reported_without_raw_transport_details() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("details that should not escape")

    with PypiClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(PypiTimeoutError, match="timed out") as error:
            client.projects.get("demo")

    assert "details that should not escape" not in str(error.value)


def test_client_config_rejects_non_https_api_urls() -> None:
    with pytest.raises(ValueError, match="HTTPS"):
        ClientConfig(api_url="http://pypi.org")


@pytest.mark.parametrize(
    "api_url",
    [
        "https://user:password@pypi.org",
        "https://pypi.org?query=value",
        "https://pypi.org/#fragment",
    ],
)
def test_client_config_rejects_credentials_queries_and_fragments(api_url: str) -> None:
    with pytest.raises(ValueError, match="HTTPS URL"):
        ClientConfig(api_url=api_url)


@pytest.mark.parametrize(
    "settings",
    [
        {"timeout": 0},
        {"timeout": float("inf")},
        {"timeout": True},
        {"max_connections": 0},
        {"max_connections": True},
        {"user_agent": "  "},
    ],
)
def test_client_config_rejects_invalid_http_settings(settings: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        ClientConfig(**settings)  # type: ignore[arg-type]


def test_client_config_strips_trailing_slash() -> None:
    assert ClientConfig(api_url="https://pypi.org/").api_url == "https://pypi.org"


def test_client_rejects_simultaneous_config_and_api_url() -> None:
    with pytest.raises(ValueError, match="config or api_url"):
        PypiClient(api_url="https://pypi.org", config=ClientConfig())


def test_closed_client_rejects_new_requests() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200)

    client = PypiClient(transport=httpx.MockTransport(handler))
    client.close()

    with pytest.raises(PypiError, match="Client is closed"):
        client.projects.get("demo")

    with pytest.raises(PypiError, match="Client is closed"):
        client.__enter__()


@pytest.mark.parametrize(
    ("feed_method", "expected_path"),
    [
        ("new_packages", "/rss/packages.xml"),
        ("latest_updates", "/rss/updates.xml"),
    ],
)
def test_global_feed_routes(
    feed_method: str, expected_path: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == expected_path
        return httpx.Response(
            200,
            text="<rss><channel><title>Recent</title></channel></rss>",
        )

    with PypiClient(transport=httpx.MockTransport(handler)) as client:
        feed = getattr(client.feeds, feed_method)()

    assert feed.title == "Recent"


@pytest.mark.parametrize("xml", ["<rss>", "<rss><not-channel /></rss>"])
def test_invalid_rss_is_reported_as_protocol_error(xml: str) -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=xml)

    with PypiClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(PypiProtocolError, match="invalid RSS"):
            client.feeds.new_packages()


@pytest.mark.parametrize(
    "lookup",
    [
        lambda client: client.projects.get(" "),
        lambda client: client.projects.get_release("demo", " "),
        lambda client: client.index.get_project(" "),
        lambda client: client.integrity.get_provenance("demo", "1.0", " "),
        lambda client: client.feeds.project_releases(" "),
    ],
)
def test_empty_identifiers_are_rejected_before_requests(lookup: object) -> None:
    with PypiClient(transport=httpx.MockTransport(lambda _: httpx.Response(200))) as client:
        with pytest.raises(ValueError, match="identifiers"):
            lookup(client)  # type: ignore[operator]
