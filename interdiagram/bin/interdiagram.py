#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

import click
import yaml

from ..models import Diagram

click.disable_unicode_literals_warning = True


# TODO: Correct documentation schema once it's frozen
@click.command()
@click.argument('yaml-file', nargs=-1, type=click.File())
@click.argument('output-file', type=click.Path(resolve_path=True))
def cli(
        yaml_file: List,
        output_file: str
) -> None:
    """Generate interaction/sitemap diagram.

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
    diagram = Diagram()
    for f in yaml_file:
        # TODO: Validate against schema
        diagram.process_spec(yaml.load(f))
    diagram.draw(output_file)


if __name__ == '__main__':
    cli()
