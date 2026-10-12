from pathlib import Path

import pytest

from meeting_cli.cli import main


def test_invalid_arguments_fail() -> None:
    with pytest.raises(SystemExit) as error:
        main([])

    assert error.value.code == 2


def test_transcribe_missing_file_returns_error(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    result = main(["transcribe", str(tmp_path / "missing.wav")])

    assert result == 1
    assert "音声ファイルが見つかりません" in capsys.readouterr().out
