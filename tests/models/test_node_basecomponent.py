# -*- coding: utf-8 -*-

from interdiagram.models.node import BaseComponent


def test_init():
    c = BaseComponent('a', 'b', 'c')
    assert c.name == 'a'
    assert c._spec == 'b'
    assert c.parent == 'c'


class TestActions:
    def test_single_action(self, input1_data):
        name = 'Experience Card'
        spec = input1_data['components'][name]
        c = BaseComponent(name, spec, 'parent')
        action = c.actions[0]
        assert len(c.actions) == 1
        assert action.name == 'Go to detail'
        assert action.port == 1

    def test_multi_actions(self, input1_data):
        name = 'Home'
        spec = input1_data['sections'][name]
        c = BaseComponent(name, spec, 'parent')
        action1, action2, action3 = c.actions
        assert len(c.actions) == 3
        assert action1.name == 'Sign up'
        assert action2.name == 'Login'
        assert action3.name == 'Search for registry'
        assert action1.port == 1
        assert action2.port == 2
        assert action3.port == 3
