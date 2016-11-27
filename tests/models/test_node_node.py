# -*- coding: utf-8 -*-

from interdiagram.models.node import Node


class MockAction:
    def render(self):
        return '<action>'


def test_init():
    c = Node('a', 'b', 'c')
    assert c.name == 'a'
    assert c._spec == 'b'
    assert c.diagram == 'c'


class TestActions:
    def test_single(self, input1_data):
        name = 'Experience Card'
        spec = input1_data['components'][name]
        c = Node(name, spec, 'diagram')
        action = c.actions[0]
        assert len(c.actions) == 1
        assert action.name == 'Go to detail'
        assert action.port == 1

    def test_multiple(self, input1_data):
        name = 'Home'
        spec = input1_data['sections'][name]
        c = Node(name, spec, 'diagram')
        action1, action2, action3 = c.actions
        assert len(c.actions) == 3
        assert action1.name == 'Sign up'
        assert action2.name == 'Login'
        assert action3.name == 'Search for registry'
        assert action1.port == 1
        assert action2.port == 2
        assert action3.port == 3

    def test_none(self, input1_data):
        name = 'Footer'
        spec = input1_data['components'][name]
        c = Node(name, spec, 'diagram')
        assert c.actions == []


class TestParts:
    def test_single(self, diagram, input1_data):
        name = 'Home'
        spec = input1_data['sections'][name]
        c = Node(name, spec, diagram)
        c1 = c.parts[0]
        expected_target = diagram.components['Experience Card']
        assert len(c.parts) == 1
        assert c1.name == 'Experience cards'
        assert c1.target == expected_target

    def test_multiple(self, diagram, input1_data):
        name = 'About'
        spec = input1_data['sections'][name]
        c = Node(name, spec, diagram)
        c1, c2 = c.parts
        expected_target = diagram.components['Footer']
        assert len(c.parts) == 2
        assert c1.name == 'Bios'
        assert c1.target is None
        assert c2.name == 'Footer'
        assert c2.target == expected_target


def test_render(mocker):
    mocker.patch(
        'interdiagram.models.node.Node.actions',
        new_callable=mocker.PropertyMock,
        return_value=[MockAction(), MockAction()]
    )
    node = Node('a', {}, 'diagram')
    expected = '<<TABLE><TR><TD PORT="0">a</TD></TR><action><action></TABLE>>'
    assert node.render() == expected
