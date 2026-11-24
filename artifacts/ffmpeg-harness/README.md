# FFmpeg Harness

An agent harness for FFmpeg — same pattern as Hermes/Claude/Codex, but for media engineering.

## Interface (like every harness)
- Input: prompt / frame sequence / image
- Process: ffmpeg pipeline (decode -> filter -> encode)
- Output: MP4 + ffprobe receipt
- Gate: HUMAN://ROOT approves before publish

## Commands (our /videogen, /animate are the harness commands)
- /videogen <images> -> Ken Burns MP4
- /animate <image> [color] -> dot particle video (first principles)
- ffmpeg direct: frames -> H.264 yuv420p faststart

## Proportions (locked)
720x1280, 30fps, crf 20, GOP 60, Level 4.1 for Android 1080x1920

## Receipts
ffprobe: codec, size, duration, bitrate — every build, no trust without verify.
