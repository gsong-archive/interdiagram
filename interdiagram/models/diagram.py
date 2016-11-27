# -*- coding: utf-8 -*-

from typing import Dict, TYPE_CHECKING

from htmlmin import minify
from jinja2 import Environment, PackageLoader
from pygraphviz import AGraph

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
        env = Environment(
            loader=PackageLoader('interdiagram', 'templates'),
            lstrip_blocks=True,
            trim_blocks=True
        )
        template = env.get_template('node.dot')

        G = AGraph(directed=True, strict=False, rankdir='LR')
        for c in self.all_components.values():
            label = minify(
                template.render(node=c),
                remove_empty_space=True,
                remove_optional_attribute_quotes=False
            )
            G.add_node(c.name, label=label, shape='none')
        G.draw(output_file, prog='dot')
        G.write()

    def process_spec(
            self,
            spec: Dict
    ) -> None:
        for k, v in spec['components'].items():
            self.add_component(k, v)
        for k, v in spec['sections'].items():
            self.add_section(k, v)
