# -*- coding: utf-8 -*-

from typing import Dict, List, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .diagram import Diagram  # noqa: F401

LooseComponent = Union[str, 'BaseComponent']


def _map_list_to_components(
        source: List[str],
        all_components: Dict[str, 'BaseComponent']
) -> List[LooseComponent]:
        components = []  # type: List[LooseComponent]
        for c in source:
            if c in all_components:
                components.append(all_components[c])
            else:
                components.append(c)
        return components


class Action:
    def __init__(
            self,
            spec: str,
            component: 'BaseComponent'
    ) -> None:
        self.name, *self._targets = spec.split('::')
        self.component = component

    @property
    def targets(self) -> List[LooseComponent]:
        targets = _map_list_to_components(
            self._targets, self.component.parent.all_components
        )
        return targets


class BaseComponent:
    def __init__(
            self,
            name: str,
            spec: Dict,
            parent: 'Diagram'
    ) -> None:
        self._spec = spec
        self.name = name
        self.parent = parent

    @property
    def actions(self) -> List['Action']:
        actions = [Action(a, self) for a in self._spec.get('actions', [])]
        return actions

    @property
    def components(self) -> List[LooseComponent]:
        components = _map_list_to_components(
            self._spec.get('components', []), self.parent.all_components
        )
        return components


class Component(BaseComponent):
    pass


class Section(BaseComponent):
    pass
