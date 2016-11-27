# -*- coding: utf-8 -*-

from interdiagram.models.node import _map_list_to_nodes


def test_map_list_to_nodes():
    source = ['a', 'b']
    all_nodes = {'a': 1}
    expected = [1, 'b']
    nodes = _map_list_to_nodes(source, all_nodes)
    assert nodes == expected
