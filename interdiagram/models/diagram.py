# -*- coding: utf-8 -*-

from typing import Dict, Union

from pygraphviz import AGraph

from .node import Component, Node, Section


def add_edge(
        graph: 'AGraph',
        source: str,
        target: Union['Node', str],
        tailport: int
) -> None:
    opts = dict(tailport=tailport)
    if isinstance(target, Node):
        opts['headport'] = 0
    graph.add_edge(source, str(target), **opts)


def add_edges(
        graph: 'AGraph',
        diagram: 'Diagram'
) -> None:
    for node in diagram.all_nodes.values():
        for action in node.actions:
            for target in action.targets:
                add_edge(graph, node.name, target, action.port)

        for part in node.parts:
            if part.target:
                add_edge(graph, node.name, part.target, part.port)


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
        G = AGraph(directed=True, strict=False, rankdir='LR')
        for node in self.all_nodes.values():
            G.add_node(node.name, label=node.render(), shape='none')
        add_edges(G, self)
        G.write()
        G.draw(output_file, prog='dot')

    def process_spec(
            self,
            spec: Dict
    ) -> None:
        for k, v in spec.get('components', {}).items():
            self.add_component(k, v)
        for k, v in spec.get('sections', {}).items():
            self.add_section(k, v)
