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
            spec: Dict[str, List[str]],
            port: int,
            component: 'BaseComponent'
    ) -> None:
        self.name, self._targets = list(spec.items())[0]
        self._targets = self._targets or []
        self.port = port
        self.component = component

    @property
    def targets(self) -> List[LooseComponent]:
        targets = _map_list_to_components(
            self._targets, self.component.parent.all_components
        )
        return targets

    def render(self) -> str:
        output = '<TR><TD PORT="{0.port}">{0.name}</TD></TR>'.format(self)
        return output


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
        actions = []
        for i, spec in enumerate(self._spec.get('actions', []), start=1):
            actions.append(Action(spec, i, self))
        return actions

    @property
    def components(self) -> List[LooseComponent]:
        components = _map_list_to_components(
            self._spec.get('components', []), self.parent.all_components
        )
        return components

    def render(self) -> str:
        name = '<TR><TD PORT="0">{}</TD></TR>'.format(self.name)
        actions = ''.join([a.render() for a in self.actions])
        output = '<<TABLE>{}{}</TABLE>>'.format(name, actions)
        return output


class Component(BaseComponent):
    pass


class Section(BaseComponent):
    pass
