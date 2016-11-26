#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from typing import List

import click

from ..models import Diagram

click.disable_unicode_literals_warning = True


@click.command()
@click.argument('json-file', nargs=-1, type=click.File())
@click.argument('output-file', type=click.Path(resolve_path=True))
def cli(json_file: List, output_file: str) -> None:
    """Generate interaction/sitemap diagram."""
    diagram = Diagram()
    for f in json_file:
        diagram.process_spec(json.load(f))
    diagram.draw(output_file)


if __name__ == '__main__':
    cli()
