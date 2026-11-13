"""Command-line entry point for basic PyPI lookups and artifact uploads."""

import argparse

from pypi_sdk.client import PypiClient
from pypi_sdk.publish import Repository, TwinePublisher


def main() -> None:
    """Run the ``pypi-sdk`` command."""
    parser = argparse.ArgumentParser(prog="pypi-sdk")
    commands = parser.add_subparsers(dest="command", required=True)

    project = commands.add_parser("project", help="show project JSON metadata")
    project.add_argument("name")

    release = commands.add_parser("release", help="show one release's metadata")
    release.add_argument("name")
    release.add_argument("version")

    upload = commands.add_parser("upload", help="upload built distributions with Twine")
    upload.add_argument("--repository", choices=("pypi", "testpypi"), required=True)
    upload.add_argument("distributions", nargs="+")

    arguments = parser.parse_args()
    if arguments.command == "upload":
        repository: Repository
        if arguments.repository == "pypi":
            repository = "pypi"
        else:
            repository = "testpypi"
        result = TwinePublisher().upload(
            arguments.distributions,
            repository=repository,
        )
        print(f"Uploaded {len(result.files)} file(s) to {result.repository}.")
        return

    with PypiClient() as client:
        if arguments.command == "project":
            response = client.projects.get(arguments.name)
        else:
            response = client.projects.get_release(arguments.name, arguments.version)
    print(response.model_dump_json(indent=2, by_alias=True, exclude_none=True))


if __name__ == "__main__":
    main()
