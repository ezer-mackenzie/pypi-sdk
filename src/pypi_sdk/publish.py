"""Safe delegation of distribution uploads to the standard Twine client."""

import os
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pypi_sdk.constants import PYPI_UPLOAD_URL, TEST_PYPI_UPLOAD_URL
from pypi_sdk.errors import PypiPublishError

Repository = Literal["pypi", "testpypi"]


@dataclass(frozen=True)
class UploadResult:
    """Summary of a successful Twine upload."""

    repository: Repository
    files: tuple[Path, ...]


class TwinePublisher:
    """Upload built distributions through Twine's supported PyPI client.

    Twine handles artifact metadata and the legacy upload protocol. It is an
    optional dependency; install ``pypi-sdk[publish]`` to use this service.
    """

    def upload(
        self,
        distributions: Iterable[str | Path],
        *,
        repository: Repository,
        token: str | None = None,
    ) -> UploadResult:
        """Upload existing build artifacts to the explicitly chosen repository.

        If ``token`` is supplied, it is passed to Twine through its standard
        environment variables and never appears in the process arguments.
        Without it, Twine may use its normal environment or Trusted Publishing
        credentials.
        """
        if repository not in ("pypi", "testpypi"):
            raise ValueError("repository must be 'pypi' or 'testpypi'")
        files = tuple(Path(item).expanduser().resolve() for item in distributions)
        if not files:
            raise ValueError("at least one distribution file is required")
        for path in files:
            if not path.is_file():
                raise ValueError(f"distribution file does not exist: {path}")
        if token is not None and not token:
            raise ValueError("token must not be empty")

        environment = os.environ.copy()
        if token is not None:
            environment["TWINE_USERNAME"] = "__token__"
            environment["TWINE_PASSWORD"] = token
        upload_url = PYPI_UPLOAD_URL if repository == "pypi" else TEST_PYPI_UPLOAD_URL
        command = [
            sys.executable,
            "-m",
            "twine",
            "upload",
            "--non-interactive",
            "--repository-url",
            upload_url,
            *(str(path) for path in files),
        ]
        result = subprocess.run(command, env=environment, check=False)
        if result.returncode != 0:
            raise PypiPublishError(
                f"Twine upload failed with exit code {result.returncode}; "
                "install the publish extra and inspect Twine's output",
                exit_code=result.returncode,
            )
        return UploadResult(repository=repository, files=files)
