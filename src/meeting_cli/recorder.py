"""Microphone recording and WAV file handling."""

from __future__ import annotations

import wave
from pathlib import Path
from typing import Any


class RecordingError(RuntimeError):
    """Raised when recording cannot be completed."""


def record_to_wav(
    output_path: Path,
    *,
    samplerate: int = 16_000,
    channels: int = 1,
    device: Any = None,
) -> Path:
    """Record microphone input until Ctrl+C and save it as PCM WAV."""
    try:
        import sounddevice as sd
    except ImportError as error:
        raise RecordingError(
            "sounddevice がインストールされていません。requirements.txt を確認してください。"
        ) from error

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frames_written = 0
    wav_file: wave.Wave_write | None = None

    try:
        wav_file = wave.open(str(output_path), "wb")
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(samplerate)

        def callback(indata: Any, frame_count: int, _time_info: Any, status: Any) -> None:
            nonlocal frames_written
            if status:
                print(f"録音デバイス: {status}")
            wav_file.writeframes(bytes(indata))
            frames_written += frame_count

        with sd.InputStream(
            samplerate=samplerate,
            channels=channels,
            dtype="int16",
            callback=callback,
            device=device,
        ):
            print("録音中です。Ctrl+C で停止します。")
            try:
                while True:
                    sd.sleep(1000)
            except KeyboardInterrupt:
                print("録音を停止しています...")
    except KeyboardInterrupt:
        pass
    except Exception as error:
        raise RecordingError(
            "マイクを開けませんでした。macOSのマイクアクセス権限と入力デバイスを確認してください。"
        ) from error
    finally:
        if wav_file is not None:
            wav_file.close()

    if frames_written == 0:
        output_path.unlink(missing_ok=True)
        raise RecordingError("録音データが空です。マイク入力を確認してください。")

    return output_path
