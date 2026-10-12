# meeting-cli

Macのマイクを録音し、ローカルでOpenAI Whisperを使って日本語の文字起こしを行うCLIです。音声とテキストは外部APIへ送信しません。

## 前提条件

- macOS
- Python 3.10以上
- Homebrew
- マイクアクセスを許可したターミナル

ffmpegとPythonの準備:

```bash
brew install ffmpeg
python3 --version
ffmpeg -version
```

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

`sounddevice` のインストールに失敗する場合は、先に `brew install portaudio` を試してください。Whisperモデルの初回利用時にはインターネット接続が必要です。

## 使い方

録音を開始し、`Ctrl+C` で停止すると自動的に文字起こしします。

```bash
meeting-cli start
```

既存の音声を文字起こしする場合:

```bash
meeting-cli transcribe recordings/2026-10-12_2100-30/audio.wav
```

Whisperモデルは `small` が既定です。速度を優先する場合は `base` などを指定できます。大きいモデルほど一般に精度が上がりますが、メモリと処理時間を多く使います。

```bash
meeting-cli start --model base
meeting-cli transcribe recordings/example/audio.wav --model base
```

モジュールとしても実行できます。

```bash
python -m meeting_cli.cli start
```

## 保存先

録音は `recordings/YYYY-MM-DD_HHMM-SS/` に保存され、次の2ファイルが作成されます。

- `audio.wav`
- `transcript.txt`

同じ秒に同名のディレクトリがある場合は連番を付けます。既存のTXTは無言で上書きしません。文字起こしが失敗しても録音ファイルは削除されません。

## マイク権限と制約

初回実行時にmacOSからマイクアクセスを求められたら許可してください。許可できない場合は「システム設定」から「プライバシーとセキュリティ」>「マイク」で、実行に使うターミナルを有効にします。

このツールはマイク入力だけを録音します。ZoomやGoogle Meetの相手の音声、システム音声の取得は対象外です。録音前に参加者へ周知し、社内ルールとプライバシーに配慮してください。音声データは機密情報を含む可能性があるため、保存・共有・削除を適切に管理してください。

Ctrl+C以外の予期しない終了やOSの強制終了では、音声ファイルが完全に保存されない可能性があります。

## テスト

実際のマイクやWhisperモデルを使わずにテストできます。

```bash
PYTHONPATH=src python -m pytest
```
