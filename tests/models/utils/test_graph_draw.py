# -*- coding: utf-8 -*-

from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from interdiagram.models.diagram import Diagram
from interdiagram.models.utils.graph import draw


@pytest.fixture
def single_diagram(input1_data):
    diagram = Diagram()
    diagram.process_spec(input1_data)
    return diagram


@pytest.fixture
def test_files():
    with TemporaryDirectory() as _tmpdir:
        tmpdir = Path(_tmpdir).resolve()
        output = tmpdir / 'o.pdf'
        log = tmpdir / 'o.out'
        yield output, log


@pytest.mark.parametrize('input', ['diagram', 'single_diagram'])
def test_draw(input, test_files, capsys, request):
    output, log = test_files
    diagram = request.getfuncargvalue(input)
    with capsys.disabled(), log.open('w+') as f, redirect_stdout(f):
        draw(diagram, str(output))
    assert output.is_file()
    assert output.stat().st_size != 0
