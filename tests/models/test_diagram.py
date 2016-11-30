# -*- coding: utf-8 -*-

import pytest

from interdiagram.models.diagram import Diagram


@pytest.fixture
def diagram():
    d = Diagram()
    return d


@pytest.fixture
def mock_add_component(diagram, mocker):
    func = mocker.patch.object(diagram, 'add_component')
    return func


@pytest.fixture
def mock_add_section(diagram, mocker):
    func = mocker.patch.object(diagram, 'add_section')
    return func


def test_add_component(diagram):
    diagram.add_component('c1', {})
    component = diagram.components['c1']
    assert 'c1' in diagram.components
    assert component.name == 'c1'
    assert component._spec == {}
    assert component.diagram == diagram


def test_add_section(diagram):
    diagram.add_section('c1', {})
    section = diagram.sections['c1']
    assert 'c1' in diagram.sections
    assert section.name == 'c1'
    assert section._spec == {}
    assert section.diagram == diagram


def test_all_nodes(diagram):
    diagram.sections = {'a': 1}
    diagram.components = {'b': 2}
    expected = {'a': 1, 'b': 2}
    assert diagram.all_nodes == expected


def test_draw(mocker):
    mock_draw = mocker.patch('interdiagram.models.diagram.draw')
    of = 'output.pdf'
    d = Diagram()
    d.draw(of)
    mock_draw.assert_called_once_with(d, of)


class TestProcessSpec:
    def test_with_components_and_sections(
            self, diagram, mock_add_component, mock_add_section
    ):
        spec = {
            'components': {'c1': 1},
            'sections': {'s1': 2},
        }
        diagram.process_spec(spec)
        mock_add_component.assert_called_once_with('c1', 1)
        mock_add_section.assert_called_once_with('s1', 2)

    def test_components_only(
            self, diagram, mock_add_component, mock_add_section
    ):
        spec = {
            'components': {'c1': 1},
        }
        diagram.process_spec(spec)
        mock_add_component.assert_called_once_with('c1', 1)
        mock_add_section.assert_not_called()

    def test_sections_only(
            self, diagram, mock_add_component, mock_add_section
    ):
        spec = {
            'sections': {'s1': 2},
        }
        diagram.process_spec(spec)
        mock_add_component.assert_not_called()
        mock_add_section.assert_called_once_with('s1', 2)
