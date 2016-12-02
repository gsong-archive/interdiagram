#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Iterable, List, TypeVar
from typing.io import IO

import click
import yaml

from ..models import Diagram

click.disable_unicode_literals_warning = True

FileType = TypeVar('FileType', IO, Path)


def _is_file_obj(
        f: FileType
) -> bool:
    read_attr = getattr(f, 'read', None)
    has_read_method = callable(read_attr)
    return has_read_method


def _draw_files(
        files: Iterable[FileType],
        output_file: str
) -> None:
    diagram = Diagram()
    for f in files:
        # TODO: Validate against schema
        if not _is_file_obj(f):
            f = f.open()  # type: ignore
        diagram.process_spec(yaml.load(f))
    diagram.draw(output_file)


# TODO: Correct documentation schema once it's frozen
@click.group()
def cli():
    """Generate interaction/sitemap diagram."""


@cli.command('dir')
@click.argument(
    'directory',
    type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
@click.argument('output-file', type=click.Path(resolve_path=True))
def directory(
        directory: str,
        output_file: str
) -> None:
    """Specify a directory where YAML files reside."""
    files = Path(directory).glob('**/*.y*ml')
    _draw_files(files, output_file)


@cli.command()
@click.argument('yaml-file', nargs=-1, type=click.File())
@click.argument('output-file', type=click.Path(resolve_path=True))
def files(
        yaml_file: List[IO],
        output_file: str
) -> None:
    """Specify individual YAML files.

    Example: interdiagram data1.yaml data2.yaml output.pdf

    The YAML spec is in the following format:

    \b
    sections:  # App sections (pages)
      Home:  # Unique key for section
        actions:  # List of call to actions
          - Sign up:  # Action name
            - Sign Up  # Reference to another section or component
          - Login:
            - Login
          - Search for registry:  # Could be empty
        components:  # List of components in this section
          - Experience cards:
            - Experience Card
    components:  # Reusable components
      Experience Card:
        actions:
          - Go to detail:
          - Add to registry:
    """
    _draw_files(yaml_file, output_file)


if __name__ == '__main__':
    cli()
