"""Paths and file handling for meeting recordings."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def create_recording_directory(base_dir: Path) -> Path:
    """Create and return a unique timestamped recording directory."""
    base_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M-%S")
    candidate = base_dir / timestamp
    suffix = 1
    while candidate.exists():
        candidate = base_dir / f"{timestamp}-{suffix}"
        suffix += 1
    candidate.mkdir()
    return candidate


def transcript_path(audio_path: Path) -> Path:
    """Return the transcript path next to an audio file."""
    return audio_path.with_suffix(".txt")


def ensure_output_does_not_exist(output_path: Path) -> None:
    """Reject an output path that would overwrite an existing file."""
    if output_path.exists():
        raise FileExistsError(f"出力ファイルは既に存在します: {output_path}")
