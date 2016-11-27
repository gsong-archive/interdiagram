# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, TYPE_CHECKING, Union

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


class Action:
    def __init__(
            self,
            spec: Dict[str, List[str]],
            port: int,
            node: 'Node'
    ) -> None:
        self.name, self._targets = list(spec.items())[0]
        self._targets = self._targets or []
        self.port = port
        self.node = node

    @property
    def targets(self) -> List[LooseNode]:
        targets = _map_list_to_nodes(
            self._targets, self.node.diagram.all_nodes
        )
        return targets

    def render(self) -> str:
        output = '<TR><TD PORT="{0.port}">{0.name}</TD></TR>'.format(self)
        return output


class Part:
    def __init__(
            self,
            spec: Dict[str, List[str]],
            node: 'Node'
    ) -> None:
        self.name, self._target = list(spec.items())[0]
        self.node = node

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
        self._spec = spec or {}
        self.name = name
        self.diagram = diagram

    @property
    def actions(self) -> List['Action']:
        actions = []
        for i, spec in enumerate(self._spec.get('actions', []), start=1):
            actions.append(Action(spec, i, self))
        return actions

    @property
    def parts(self) -> List[LooseNode]:
        parts = []
        for spec in self._spec.get('parts', []):
            parts.append(Part(spec, self))
        return parts

    def render(self) -> str:
        name = '<TR><TD PORT="0">{}</TD></TR>'.format(self.name)
        actions = ''.join([a.render() for a in self.actions])
        output = '<<TABLE>{}{}</TABLE>>'.format(name, actions)
        return output


class Component(Node):
    pass


class Section(Node):
    pass
