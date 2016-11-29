# -*- coding: utf-8 -*-

from typing import Callable, Dict, List, Optional, TYPE_CHECKING, Union

from .typing import NodeAttr
from .utils.graph import render_node, render_node_attribute

if TYPE_CHECKING:
    from .diagram import Diagram  # noqa: F401

LooseNode = Union[str, 'Node']


def _map_list_to_nodes(
        source: List[str],
        all_nodes: Dict[str, 'Node']
) -> List[LooseNode]:
        nodes = []  # type: List[LooseNode]
        for c in source:
            if c in all_nodes:
                nodes.append(all_nodes[c])
            else:
                nodes.append(c)
        return nodes


class NodeAttribute:
    def __init__(
            self,
            spec: Dict,
            port: int,
            node: 'Node'
    ) -> None:
        self.name, self._targets = list(spec.items())[0]
        self._targets = self._targets or []
        self.port = port
        self.node = node

    def render(self) -> str:
        output = render_node_attribute(self.name, self.port)
        return output


class Action(NodeAttribute):
    @property
    def targets(self) -> List[LooseNode]:
        targets = _map_list_to_nodes(
            self._targets, self.node.diagram.all_nodes
        )
        return targets


class Part(NodeAttribute):
    def __init__(
            self,
            spec: Dict[str, str],
            port: int,
            node: 'Node'
    ) -> None:
        super().__init__(spec, port, node)
        self._target = self._targets or None

    @property
    def target(self) -> LooseNode:
        target = _map_list_to_nodes(
            [self._target], self.node.diagram.all_nodes
        )[0]
        return target


class Node:
    def __init__(
            self,
            name: str,
            spec: Optional[Dict],
            diagram: 'Diagram'
    ) -> None:
        self._actions = None  # type: Optional[List[Action]]
        self._parts = None  # type: Optional[List[Part]]
        self._spec = spec or {}
        self.diagram = diagram
        self.name = name
        self.next_port = 1

    def __str__(self) -> str:
        return self.name

    def _generate_list(
            self,
            key: str,
            klass: Callable[..., NodeAttr]
    ) -> List[NodeAttr]:
        objs = []
        for i, spec in enumerate(
                self._spec.get(key, []), start=self.next_port
        ):
            objs.append(klass(spec, i, self))
            self.next_port += 1
        return objs

    @property
    def actions(self) -> List['Action']:
        if getattr(self, '_actions', None) is not None:
            return self._actions
        self._actions = self._generate_list('actions', Action)
        return self._actions

    @property
    def parts(self) -> List[Part]:
        if getattr(self, '_parts', None) is not None:
            return self._parts
        self._parts = self._generate_list('parts', Part)
        return self._parts

    def render(self) -> str:
        output = render_node(self)
        return output
