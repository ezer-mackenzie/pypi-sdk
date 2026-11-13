"""SDK exceptions with sanitized HTTP context."""


class PypiError(Exception):
    """Base exception for PyPI SDK failures."""


class PypiHTTPError(PypiError):
    """PyPI returned an unsuccessful HTTP response."""

    def __init__(self, message: str, *, status_code: int, endpoint: str) -> None:
        super().__init__(message)
        self.status_code: int = status_code
        self.endpoint: str = endpoint


class PypiAuthenticationError(PypiHTTPError):
    """The request requires valid authentication."""


class PypiAuthorizationError(PypiHTTPError):
    """The authenticated caller is not allowed to perform this request."""


class PypiNotFoundError(PypiHTTPError):
    """The requested PyPI resource does not exist."""


class PypiRateLimitError(PypiHTTPError):
    """PyPI rejected the request due to rate limiting."""


class PypiConnectionError(PypiError):
    """The HTTP request could not be completed."""


class PypiTimeoutError(PypiError):
    """The HTTP request timed out."""


class PypiProtocolError(PypiError):
    """PyPI returned data that did not match the documented response format."""


class PypiPublishError(PypiError):
    """Twine could not publish the requested distributions."""

    def __init__(self, message: str, *, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code: int = exit_code
