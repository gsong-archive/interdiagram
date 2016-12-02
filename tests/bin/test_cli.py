# -*- coding: utf-8 -*-

from pathlib import Path
from tempfile import TemporaryDirectory

from click.testing import CliRunner

from interdiagram.bin.interdiagram import cli


def test_files(input1, input2, input1_data, input2_data, mocker):
    runner = CliRunner()
    mock_process_spec = mocker.patch(
        'interdiagram.bin.interdiagram.Diagram.process_spec'
    )
    mock_draw = mocker.patch('interdiagram.bin.interdiagram.Diagram.draw')

    with TemporaryDirectory() as _tmpdir:
        tmpdir = Path(_tmpdir).resolve()
        output = (tmpdir / 'o.pdf').as_posix()
        args = ['files', input1, input2, output]
        result = runner.invoke(cli, args)

        assert result.exit_code == 0
        assert mock_process_spec.call_count == 2
        mock_process_spec.assert_any_call(input1_data)
        mock_process_spec.assert_called_with(input2_data)
        mock_draw.assert_called_once_with(output)
