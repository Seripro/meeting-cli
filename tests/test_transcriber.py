from pathlib import Path

import pytest

from meeting_cli.transcriber import TranscriptionError, transcribe_file


class FakeModel:
    def transcribe(self, _audio_path: str, **kwargs: object) -> dict[str, str]:
        assert kwargs == {"language": "ja", "verbose": True}
        return {"text": "これは会議の文字起こしです。"}


def test_transcribe_writes_utf8_text(tmp_path: Path) -> None:
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"wav data")

    output = transcribe_file(audio, model=FakeModel())

    assert output.read_text(encoding="utf-8") == "これは会議の文字起こしです。"


def test_missing_audio_is_a_clear_error(tmp_path: Path) -> None:
    with pytest.raises(TranscriptionError, match="見つかりません"):
        transcribe_file(tmp_path / "missing.wav", model=FakeModel())


def test_transcription_failure_does_not_delete_audio(tmp_path: Path) -> None:
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"wav data")

    class FailingModel:
        def transcribe(self, audio_path: str, **kwargs: object) -> dict[str, str]:
            raise RuntimeError("decode failed")

    with pytest.raises(TranscriptionError):
        transcribe_file(audio, model=FailingModel())

    assert audio.exists()
    assert not (tmp_path / "audio.txt").exists()


def test_existing_transcript_is_not_overwritten(tmp_path: Path) -> None:
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"wav data")
    transcript = tmp_path / "audio.txt"
    transcript.write_text("original", encoding="utf-8")

    with pytest.raises(FileExistsError):
        transcribe_file(audio, model=FakeModel())

    assert transcript.read_text(encoding="utf-8") == "original"
