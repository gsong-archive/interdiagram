# -*- coding: utf-8 -*-

from pathlib import Path
from tempfile import gettempdir

from click.testing import CliRunner

from interdiagram.bin.interdiagram import Diagram, cli

OUTPUT = Path(gettempdir()).resolve().joinpath('o.pdf').as_posix()


def test_cli(input1, input2, input1_data, input2_data, mocker):
    runner = CliRunner()
    mock_process_spec = mocker.patch.object(Diagram, 'process_spec')
    mock_draw = mocker.patch.object(Diagram, 'draw')

    args = [input1, input2, OUTPUT]
    result = runner.invoke(cli, args)

    assert result.exit_code == 0
    assert mock_process_spec.call_count == 2
    mock_process_spec.assert_any_call(input1_data)
    mock_process_spec.assert_called_with(input2_data)
    mock_draw.assert_called_once_with(OUTPUT)
