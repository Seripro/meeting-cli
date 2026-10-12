from pathlib import Path

import pytest

from meeting_cli.storage import (
    create_recording_directory,
    ensure_output_does_not_exist,
    transcript_path,
)


def test_create_recording_directory_uses_unique_timestamped_names(tmp_path: Path) -> None:
    first = create_recording_directory(tmp_path)
    second = create_recording_directory(tmp_path)

    assert first.is_dir()
    assert second.is_dir()
    assert first != second
    assert first.name.startswith("20")


def test_transcript_path_replaces_only_extension(tmp_path: Path) -> None:
    assert transcript_path(tmp_path / "audio.wav") == tmp_path / "audio.txt"


def test_existing_output_is_rejected(tmp_path: Path) -> None:
    output = tmp_path / "transcript.txt"
    output.touch()

    with pytest.raises(FileExistsError):
        ensure_output_does_not_exist(output)
