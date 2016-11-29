# -*- coding: utf-8 -*-

from typing import List, TYPE_CHECKING, Tuple, Union

from pygraphviz import AGraph

from ..typing import NodeAttr
from .options import *

if TYPE_CHECKING:
    from ..diagram import Diagram  # noqa: F401
    from ..node import Node  # noqa: F401


def _add_edge(
        graph: 'AGraph',
        source: str,
        target: Union['Node', str],
        tailport: int
) -> None:
    from ..node import Node  # noqa: F811

    opts = dict(tailport=tailport, **EDGE_OPTIONS)
    if isinstance(target, Node):
        opts['headport'] = 0
    else:
        graph.add_node(target, **AD_HOC_NODE_OPTIONS)
    graph.add_edge(source, str(target), **opts)


def _render_node_headers(node: 'Node') -> Tuple[str, str]:
    template = (
        '<TR><TD ALIGN="LEFT" COLSPAN="2">'
        '<FONT COLOR="{}">{{}}:</FONT>'
        '</TD></TR>'
    ).format(GRAY)

    actions_header = ''
    if node.actions:
        actions_header = template.format('Actions')
    parts_header = ''
    if node.parts:
        parts_header = template.format('Attributes')
    return actions_header, parts_header


def _render_node_name(node: 'Node') -> str:
    output = (
        '<TR><TD PORT="0" ALIGN="CENTER" COLSPAN="2">'
        '<FONT FACE="{}">{}</FONT>'
        '</TD></TR>'
    ).format(FONT_BOLD, node.name)
    return output


def _render_section_details(details: List[NodeAttr]) -> str:
    output = ''.join([o.render() for o in details])
    return output


def add_edges(
        graph: 'AGraph',
        diagram: 'Diagram'
) -> None:
    for node in diagram.all_nodes.values():
        for action in node.actions:
            for target in action.targets:
                _add_edge(graph, node.name, target, action.port)

        for part in node.parts:
            if part.target:
                _add_edge(graph, node.name, part.target, part.port)


def draw(
        diagram: 'Diagram',
        output_file: 'str'
) -> None:
    G = AGraph(**GRAPH_OPTIONS)
    for node in diagram.components.values():
        G.add_node(node.name, label=node.render(), **COMPONENT_OPTIONS)
    for node in diagram.sections.values():
        G.add_node(node.name, label=node.render(), **SECTION_OPTIONS)
    add_edges(G, diagram)
    G.write()
    G.draw(output_file, prog=LAYOUT)


def render_node(node: 'Node') -> str:
    name = _render_node_name(node)
    actions_header, parts_header = _render_node_headers(node)
    actions = _render_section_details(node.actions)
    parts = _render_section_details(node.parts)

    actions = ''.join([o.render() for o in node.actions])
    parts = ''.join([o.render() for o in node.parts])
    output = (
        '<<TABLE BORDER="0" ROWS="*">'
        '{name}'
        '{parts_header}{parts}'
        '{actions_header}{actions}'
        '</TABLE>>'
    ).format(**locals())
    return output


def render_node_attribute(
        name: str,
        port: int
) -> str:
    output = (
        '<TR><TD></TD><TD PORT="{port}" ALIGN="LEFT">{name}</TD></TR>'
    ).format(**locals())
    return output
