"""Whisper-based Japanese transcription."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from .storage import ensure_output_does_not_exist, transcript_path


class TranscriptionError(RuntimeError):
    """Raised when an audio file cannot be transcribed."""


@lru_cache(maxsize=None)
def _load_model(model_name: str) -> Any:
    try:
        import whisper
    except ImportError as error:
        raise TranscriptionError(
            "openai-whisper がインストールされていません。requirements.txt を確認してください。"
        ) from error

    print(f"Whisperモデル '{model_name}' を読み込んでいます。初回はダウンロードに時間がかかります。")
    try:
        return whisper.load_model(model_name)
    except Exception as error:
        raise TranscriptionError(f"Whisperモデルの読み込みに失敗しました: {error}") from error


def transcribe_file(
    audio_path: Path,
    *,
    model_name: str = "small",
    output_path: Path | None = None,
    model: Any = None,
) -> Path:
    """Transcribe an audio file in Japanese and save UTF-8 text beside it."""
    if not audio_path.exists():
        raise TranscriptionError(f"音声ファイルが見つかりません: {audio_path}")
    if not audio_path.is_file() or audio_path.stat().st_size == 0:
        raise TranscriptionError(f"音声ファイルが空か、読み込めません: {audio_path}")

    destination = output_path or transcript_path(audio_path)
    ensure_output_does_not_exist(destination)
    recognizer = model or _load_model(model_name)

    print("文字起こし中です...")
    try:
        result = recognizer.transcribe(str(audio_path), language="ja", verbose=True)
        text = result["text"]
    except Exception as error:
        raise TranscriptionError(f"文字起こしに失敗しました: {error}") from error

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    return destination
