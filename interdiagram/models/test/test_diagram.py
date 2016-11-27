# -*- coding: utf-8 -*-

import pytest

from interdiagram.models.diagram import Diagram


@pytest.fixture
def diagram():
    d = Diagram()
    return d


def test_all_components(diagram):
    diagram.sections = {'a': 1}
    diagram.components = {'b': 2}
    expected = {'a': 1, 'b': 2}
    assert diagram.all_components == expected


def test_process_spec(diagram, mocker):
    mock_add_component = mocker.patch.object(diagram, 'add_component')
    mock_add_section = mocker.patch.object(diagram, 'add_section')
    spec = {
        'components': {'c1': 1},
        'sections': {'s1': 2}
    }
    diagram.process_spec(spec)
    mock_add_component.assert_called_once_with('c1', 1)
    mock_add_section.assert_called_once_with('s1', 2)
