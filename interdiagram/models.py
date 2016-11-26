# -*- coding: utf-8 -*-

from typing import Dict, List, Union

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
