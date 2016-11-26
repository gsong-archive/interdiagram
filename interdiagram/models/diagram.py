# -*- coding: utf-8 -*-

from typing import Dict, TYPE_CHECKING

from .node import Component, Section

if TYPE_CHECKING:
    from .node import BaseComponent  # noqa: F401


class Diagram:
    def __init__(self) -> None:
        self.sections = {}  # type: Dict
        self.components = {}  # type: Dict

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

    @property
    def all_components(self) -> Dict[str, 'BaseComponent']:
        all = dict(self.sections)
        all.update(self.components)
        return all

    def draw(
            self,
            output_file: str
    ) -> None:
        for c in self.components.values():
            print(
                c.name, [(a.name, a.targets) for a in c.actions], c.components
            )

        for c in self.sections.values():
            print(
                c.name, [(a.name, a.targets) for a in c.actions], c.components
            )

    def process_spec(
            self,
            spec: Dict
    ) -> None:
        for k, v in spec['components'].items():
            self.add_component(k, v)
        for k, v in spec['sections'].items():
            self.add_section(k, v)
