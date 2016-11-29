# -*- coding: utf-8 -*-

from pygraphviz import AGraph
import pytest

from interdiagram.models.node import Node
from interdiagram.models.utils.graph import _add_edge, add_edges
from interdiagram.models.utils.options import *


@pytest.fixture
def mock_graph_add_edge(mocker):
    func = mocker.patch('pygraphviz.AGraph.add_edge')
    return func


class TestAddEdge:
    def test_node_target(self, mock_graph_add_edge, mocker):
        name = 'mocked node'
        mocker.patch.object(Node, '__str__', return_value=name)

        source = 'source'
        target = Node(name, {}, 'diagram')
        tailport = 1

        _add_edge(AGraph(), source, target, tailport)
        options = dict(tailport=tailport, headport=0, **EDGE_OPTIONS)
        mock_graph_add_edge.assert_called_once_with(source, name, **options)

    def test_str_target(self, mock_graph_add_edge, mocker):
        mock_graph_add_node = mocker.patch('pygraphviz.AGraph.add_node')
        source = 'source'
        target = 'target'
        tailport = 1

        _add_edge(AGraph(), source, target, tailport)
        opts = dict(tailport=tailport, **EDGE_OPTIONS)
        mock_graph_add_node.assert_called_once_with(
            target, **AD_HOC_NODE_OPTIONS
        )
        mock_graph_add_edge.assert_called_once_with(source, target, **opts)


def test_add_edges(diagram, mocker):
    mock_add_edge = mocker.patch('interdiagram.models.utils.graph._add_edge')
    add_edges('graph', diagram)
    assert mock_add_edge.call_count == 10

    card = diagram.all_nodes['Experience Card']
    footer = diagram.all_nodes['Footer']
    home = diagram.all_nodes['Home']
    login = diagram.all_nodes['Login']
    sign_up = diagram.all_nodes['Sign Up']
    calls = [
        mocker.call('graph', 'About', footer, 2),
        mocker.call('graph', 'Home', sign_up, 1),
        mocker.call('graph', 'Home', login, 2),
        mocker.call('graph', 'Home', card, 4),
        mocker.call('graph', 'Login', home, 2),
        mocker.call('graph', 'Login', sign_up, 3),
        mocker.call('graph', 'Login', 'Bar', 4),
        mocker.call('graph', 'Sign Up', 'Email User', 1),
        mocker.call('graph', 'Sign Up', login, 1),
        mocker.call('graph', 'Sign Up', home, 2),
    ]
    mock_add_edge.assert_has_calls(calls, any_order=True)
