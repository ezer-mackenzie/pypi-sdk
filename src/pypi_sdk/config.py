"""Configuration for the synchronous PyPI client."""

import math
from dataclasses import dataclass
from urllib.parse import urlsplit

from pypi_sdk.constants import DEFAULT_API_URL, DEFAULT_USER_AGENT


@dataclass(frozen=True)
class ClientConfig:
    """Validated, non-secret HTTP settings for :class:`PypiClient`."""

    api_url: str = DEFAULT_API_URL
    user_agent: str = DEFAULT_USER_AGENT
    timeout: float = 30.0
    max_connections: int = 20

    def __post_init__(self) -> None:
        parsed = urlsplit(self.api_url)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("api_url must be an HTTPS URL without credentials, query, or fragment")
        if type(self.timeout) is bool or not math.isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError("timeout must be a finite positive number")
        if type(self.max_connections) is not int or self.max_connections < 1:
            raise ValueError("max_connections must be a positive integer")
        if not self.user_agent.strip():
            raise ValueError("user_agent must not be empty")
        object.__setattr__(self, "api_url", self.api_url.rstrip("/"))

    def __repr__(self) -> str:
        return (
            f"ClientConfig(api_url={self.api_url!r}, user_agent={self.user_agent!r}, "
            f"timeout={self.timeout!r}, max_connections={self.max_connections!r})"
        )
