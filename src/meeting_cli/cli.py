"""Command-line interface for meeting-cli."""

from __future__ import annotations

import argparse
from pathlib import Path

from .recorder import RecordingError, record_to_wav
from .storage import create_recording_directory
from .transcriber import TranscriptionError, transcribe_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="meeting-cli",
        description="マイク録音とローカルWhisper文字起こしを行います。",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="録音してから文字起こしします")
    start_parser.add_argument("--model", default="small", help="Whisperモデル名 (既定: small)")
    start_parser.add_argument(
        "--recordings-dir",
        type=Path,
        default=Path("recordings"),
        help="録音保存先 (既定: recordings)",
    )

    transcribe_parser = subparsers.add_parser("transcribe", help="既存の音声を文字起こしします")
    transcribe_parser.add_argument("audio", type=Path, help="文字起こしする音声ファイル")
    transcribe_parser.add_argument("--model", default="small", help="Whisperモデル名 (既定: small)")
    return parser


def _run_start(args: argparse.Namespace) -> int:
    try:
        recording_dir = create_recording_directory(args.recordings_dir)
        audio_path = recording_dir / "audio.wav"
        record_to_wav(audio_path)
        print(f"録音を保存しました: {audio_path.resolve()}")
    except RecordingError as error:
        print(f"エラー: {error}")
        return 1

    try:
        transcript = transcribe_file(audio_path, model_name=args.model)
    except (TranscriptionError, FileExistsError) as error:
        print(f"エラー: {error}")
        print(f"録音ファイルは残っています: {audio_path.resolve()}")
        return 1

    print(f"文字起こしを保存しました: {transcript.resolve()}")
    print("完了")
    return 0


def _run_transcribe(args: argparse.Namespace) -> int:
    try:
        transcript = transcribe_file(args.audio, model_name=args.model)
    except (TranscriptionError, FileExistsError) as error:
        print(f"エラー: {error}")
        return 1

    print(f"文字起こしを保存しました: {transcript.resolve()}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "start":
        return _run_start(args)
    return _run_transcribe(args)


if __name__ == "__main__":
    raise SystemExit(main())
