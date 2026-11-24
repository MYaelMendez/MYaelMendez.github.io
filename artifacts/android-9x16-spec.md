# Mobile 9:16 — Android MCP optimization

## Video spec (Android-first)
- Resolution: 1080x1920 (master 720x1280 for preview)
- Codec: H.264 High Profile, yuv420p, Level 4.1+
- Bitrate: 6-10 Mbps (1080x1920) / 2-4 Mbps (720x1280 preview)
- FPS: 30 (60 for re-encode)
- Audio: AAC 128kbps 48kHz (when present)
- Faststart: yes (moov before mdat, instant mobile playback)
- GOP: 60 (2s keyframes for seek/scrub)

## FFmpeg recipe
ffmpeg -i in.mp4 -vf scale=1080:1920 -c:v libx264 -profile:v high -level 4.1 -pix_fmt yuv420p -b:v 8M -maxrate 10M -bufsize 16M -g 60 -c:a aac -b:a 128k -ar 48000 -movflags +faststart out-android.mp4

## MCP layer (Android MCP server)
- Serve MP4 via authenticated HTTP with Range support (206 Partial Content)
- Poster PNG (360x640) for instant preview, lazy-load video
- Content-Type: video/mp4, Accept-Ranges: bytes
- File size cap: <15MB for 9s @1080x1920
