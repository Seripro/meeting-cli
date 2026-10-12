from pathlib import Path

import pytest

from meeting_cli.recorder import RecordingError, record_to_wav


class FakeInputStream:
    def __init__(self, *, callback, **_kwargs):
        self.callback = callback

    def __enter__(self):
        self.callback(b"\x00\x00" * 4, 4, None, None)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


def test_keyboard_interrupt_closes_a_valid_wav(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    class FakeSoundDevice:
        InputStream = FakeInputStream

        @staticmethod
        def sleep(milliseconds: int) -> None:
            raise KeyboardInterrupt

    monkeypatch.setitem(__import__("sys").modules, "sounddevice", FakeSoundDevice())

    output = record_to_wav(tmp_path / "audio.wav")

    assert output.exists()
    assert output.read_bytes().startswith(b"RIFF")


def test_empty_recording_is_removed(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    class FakeSoundDevice:
        class InputStream:
            def __init__(self, **kwargs):
                pass

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                return False

        @staticmethod
        def sleep(milliseconds: int) -> None:
            raise KeyboardInterrupt

    monkeypatch.setitem(__import__("sys").modules, "sounddevice", FakeSoundDevice())

    with pytest.raises(RecordingError):
        record_to_wav(tmp_path / "audio.wav")

    assert not (tmp_path / "audio.wav").exists()
