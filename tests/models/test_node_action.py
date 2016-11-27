# -*- coding: utf-8 -*-

from interdiagram.models.node import Action


def _prep_action(
        data, diagram, port, section, action_index, part='sections'
):
    spec = data[part][section]['actions'][action_index]
    node = getattr(diagram, part)[section]
    action = Action(spec, port, node)
    return spec, node, action


class TestInit:
    port = 1
    node = 'x'

    def test_init(self):
        spec = {'a': [1]}
        action = Action(spec, self.port, self.node)
        assert action.name == 'a'
        assert action._targets == [1]
        assert action.port == self.port
        assert action.node == self.node

    def test_empty_spec(self):
        spec = {'a': None}
        action = Action(spec, self.port, self.node)
        assert action.name == 'a'
        assert action._targets == []
        assert action.port == self.port
        assert action.node == self.node


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
    expected = '<TR><TD PORT="1">a</TD></TR>'
    assert action.render() == expected
