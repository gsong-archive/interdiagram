# -*- coding: utf-8 -*-

from pathlib import Path

from click.testing import CliRunner
import yaml

from interdiagram.bin import interdiagram

HERE = Path(__file__).parent
INPUT1 = HERE.joinpath('data/data1.yaml')
INPUT2 = HERE.joinpath('data/data2.yaml')
OUTPUT = HERE.joinpath('output.pdf')

with INPUT1.open() as f:
    INPUT1_CONTENT = yaml.load(f)

with INPUT2.open() as f:
    INPUT2_CONTENT = yaml.load(f)


def test_cli(mocker):
    runner = CliRunner()
    mock_process_spec = mocker.patch.object(
        interdiagram.Diagram, 'process_spec'
    )
    mock_draw = mocker.patch.object(interdiagram.Diagram, 'draw')

    args = [INPUT1.as_posix(), INPUT2.as_posix(), OUTPUT.as_posix()]
    result = runner.invoke(interdiagram.cli, args)

    assert result.exit_code == 0
    assert mock_process_spec.call_count == 2
    mock_process_spec.assert_any_call(INPUT1_CONTENT)
    mock_process_spec.assert_called_with(INPUT2_CONTENT)
    mock_draw.assert_called_once_with(OUTPUT.as_posix())
