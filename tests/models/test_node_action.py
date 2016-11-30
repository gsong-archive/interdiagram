# -*- coding: utf-8 -*-

import pytest

from interdiagram.models.node import Action


def _prep_action(
        data, diagram, port, section, action_index, part='sections'
):
    spec = data[part][section]['actions'][action_index]
    node = getattr(diagram, part)[section]
    action = Action(spec, port, node)
    return spec, node, action


@pytest.mark.parametrize('targets, expected', [
    ([1],) * 2,
    ([1, 2],) * 2,
    (None, []),
])
def test_init(targets, expected):
    node = 'x'
    port = 1
    spec = {'a': targets}
    action = Action(spec, port, node)
    assert action.name == 'a'
    assert action._targets == expected
    assert action.port == port
    assert action.node == node


class TestTargets:
    port = 1

    def test_ref(self, diagram, input2_data):
        spec, node, action = _prep_action(
            input2_data, diagram, self.port, 'Login', 1
        )
        expected = [diagram.sections['Home']]
        assert action.targets == expected

    def test_noref(self, diagram, input2_data):
        spec, node, action = _prep_action(
            input2_data, diagram, self.port, 'Login', 3
        )
        expected = spec['Foo']
        assert action.targets == expected

    def test_empty(self, diagram, input1_data):
        spec, node, action = _prep_action(
            input1_data, diagram, self.port, 'Experience Card', 0, 'components'
        )
        assert action.targets == []

    def test_multiple(self, diagram, input2_data):
        spec, node, action = _prep_action(
            input2_data, diagram, self.port, 'Sign Up', 0
        )
        expected = ['Email User', diagram.sections['Login']]
        assert action.targets == expected


def test_render():
    spec = {'a': [1]}
    action = Action(spec, 1, 'x')
    expected = '<TR><TD></TD><TD PORT="1" ALIGN="LEFT">a</TD></TR>'
    assert action.render() == expected
