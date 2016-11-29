# -*- coding: utf-8 -*-

from typing import Dict, TYPE_CHECKING

from .node import Component, Section
from .utils.graph import draw

if TYPE_CHECKING:
    from .node import Node  # noqa: F401


class Diagram:
    def __init__(self) -> None:
        self.sections = {}  # type: Dict
        self.components = {}  # type: Dict

    @property
    def all_nodes(self) -> Dict[str, 'Node']:
        all = dict(self.sections)
        all.update(self.components)
        return all

    def add_component(
            self,
            name: str,
            spec: Dict
    ) -> None:
        self.components[name] = Component(name, spec, self)

    def add_section(
            self,
            name: str,
            spec: Dict
    ) -> None:
        self.sections[name] = Section(name, spec, self)

    def draw(
            self,
            output_file: str
    ) -> None:  # pragma: no cover
        draw(self, output_file)

    def process_spec(
            self,
            spec: Dict
    ) -> None:
        for k, v in spec.get('components', {}).items():
            self.add_component(k, v)
        for k, v in spec.get('sections', {}).items():
            self.add_section(k, v)
