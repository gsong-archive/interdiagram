# -*- coding: utf-8 -*-

from interdiagram.models.node import _map_list_to_components


def test_map_list_to_components():
    source = ['a', 'b']
    all_components = {'a': 1}
    expected = [1, 'b']
    components = _map_list_to_components(source, all_components)
    assert components == expected
