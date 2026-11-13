"""Synchronous clients for PyPI's documented APIs."""

from types import TracebackType
from typing import Self, TypeVar

import httpx
from pydantic import BaseModel

from pypi_sdk.config import ClientConfig
from pypi_sdk.errors import (
    PypiAuthenticationError,
    PypiAuthorizationError,
    PypiConnectionError,
    PypiError,
    PypiHTTPError,
    PypiNotFoundError,
    PypiProtocolError,
    PypiRateLimitError,
    PypiTimeoutError,
)
from pypi_sdk.models import (
    ProjectResponse,
    ProvenanceResponse,
    SimpleProjectResponse,
    SimpleProjectsResponse,
    StatsResponse,
)
from pypi_sdk.publish import TwinePublisher
from pypi_sdk.services import (
    FeedService,
    IndexService,
    IntegrityService,
    ProjectService,
    StatsService,
    parse_model,
)

ModelT = TypeVar("ModelT", bound=BaseModel)


class PypiClient:
    """Reusable synchronous client for PyPI's public APIs.

    Requests are anonymous, redirects are not followed, and requests are never
    retried automatically. Upload credentials are scoped to the publisher and
    are not sent to PyPI's read APIs.
    """

    def __init__(
        self,
        api_url: str | None = None,
        *,
        config: ClientConfig | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if config is not None and api_url is not None:
            raise ValueError("Pass config or api_url, not both")
        if config is None:
            config = ClientConfig(api_url=api_url) if api_url is not None else ClientConfig()
        self.config: ClientConfig = config
        self._http = httpx.Client(
            headers={"User-Agent": config.user_agent},
            timeout=httpx.Timeout(config.timeout),
            limits=httpx.Limits(
                max_connections=config.max_connections,
                max_keepalive_connections=config.max_connections,
            ),
            follow_redirects=False,
            trust_env=False,
            transport=transport,
        )
        self.projects: ProjectService = ProjectService(
            lambda path, accept: self._get_json(path, accept, ProjectResponse)
        )
        self.index: IndexService = IndexService(
            lambda path, accept: self._get_json(path, accept, SimpleProjectsResponse),
            lambda path, accept: self._get_json(path, accept, SimpleProjectResponse),
        )
        self.integrity: IntegrityService = IntegrityService(
            lambda path, accept: self._get_json(path, accept, ProvenanceResponse)
        )
        self.stats: StatsService = StatsService(
            lambda path, accept: self._get_json(path, accept, StatsResponse)
        )
        self.feeds: FeedService = FeedService(self._get_text)
        self.publisher: TwinePublisher = TwinePublisher()

    @property
    def is_closed(self) -> bool:
        """Whether the owned HTTP client has been closed."""
        return self._http.is_closed

    def close(self) -> None:
        """Release the connection pool; safe to call more than once."""
        self._http.close()

    def __enter__(self) -> Self:
        if self.is_closed:
            raise PypiError("Client is closed")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def _get_json(self, path: str, accept: str, model_type: type[ModelT]) -> ModelT:
        response = self._get(path, accept)
        try:
            payload = response.json()
        except (ValueError, UnicodeDecodeError):
            raise PypiProtocolError("PyPI returned invalid JSON") from None
        return parse_model(model_type, payload)

    def _get_text(self, path: str, accept: str) -> str:
        return self._get(path, accept).text

    def _get(self, path: str, accept: str) -> httpx.Response:
        if self.is_closed:
            raise PypiError("Client is closed")
        try:
            response = self._http.get(
                self.config.api_url + path,
                headers={"Accept": accept},
            )
        except httpx.TimeoutException:
            raise PypiTimeoutError("PyPI request timed out") from None
        except httpx.RequestError:
            raise PypiConnectionError("PyPI request could not complete") from None
        if not response.is_success:
            self._raise_http_error(response.status_code, path)
        return response

    @staticmethod
    def _raise_http_error(status_code: int, endpoint: str) -> None:
        message = f"PyPI returned HTTP {status_code}"
        error_type: type[PypiHTTPError]
        if status_code == 401:
            error_type = PypiAuthenticationError
        elif status_code == 403:
            error_type = PypiAuthorizationError
        elif status_code == 404:
            error_type = PypiNotFoundError
        elif status_code == 429:
            error_type = PypiRateLimitError
        else:
            error_type = PypiHTTPError
        raise error_type(message, status_code=status_code, endpoint=endpoint)
