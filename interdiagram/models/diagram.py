# -*- coding: utf-8 -*-

from typing import Dict

from .node import Node
from .utils.graph import draw


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
        self.components[name] = Node(name, spec, self)

    def add_section(
            self,
            name: str,
            spec: Dict
    ) -> None:
        self.sections[name] = Node(name, spec, self)

    def draw(
            self,
            output_file: str
    ) -> None:
        draw(self, output_file)

    def process_spec(
            self,
            spec: Dict
    ) -> None:
        for k, v in spec.get('components', {}).items():
            self.add_component(k, v)
        for k, v in spec.get('sections', {}).items():
            self.add_section(k, v)
