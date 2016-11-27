# -*- coding: utf-8 -*-

from pathlib import Path

import pytest
import yaml

from interdiagram.models.diagram import Diagram

HERE = Path(__file__).parent
INPUT1 = HERE.joinpath('data/data1.yaml')
INPUT2 = HERE.joinpath('data/data2.yaml')


def _load(p):
    with p.open() as f:
        content = yaml.load(f)
    return content


@pytest.fixture
def diagram(input1_data, input2_data):
    d = Diagram()
    d.process_spec(input1_data)
    d.process_spec(input2_data)
    return d


@pytest.fixture
def input1():
    return INPUT1.as_posix()


@pytest.fixture
def input1_data():
    return _load(INPUT1)


@pytest.fixture
def input2():
    return INPUT2.as_posix()


@pytest.fixture
def input2_data():
    return _load(INPUT2)
