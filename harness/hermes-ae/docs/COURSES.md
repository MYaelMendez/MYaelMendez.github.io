# Open Courses

Open courses use the OpenSourceWare two-voice template:

- **F2 / nous girl** = root voice — asks, challenges, and holds authority.
- **M2 / hermes-agent** = build voice — explains, demonstrates, and summarizes.

A lesson is a JSON file under `courses/`. Copy `courses/template.json`, set
`id`, `title`, `principle`, and the `segments` list, then run:

```bash
python scripts/course_video.py --lesson courses/osw-101.json
```

The generator:

1. synthesizes each segment with tiny-voca at the requested voice and speed;
2. joins the WAVs with timed gaps and pads to the planned duration;
3. paints deterministic 720×1280 captions, voice labels, and waveform frames;
4. assembles H.264 + AAC with ffmpeg;
5. runs a QC gate (`ffprobe`, `volumedetect`, bright-pixel check);
6. writes a `COURSE://<ID>` `HUMAN://ROOT` receipt;
7. removes the frame cache unless `--no-cleanup` is passed.

Output defaults to the configured runtime path:
`$HERMES_AE_HOME/asimov-anim/courses/<id>/<id>-916.mp4`.

Publishing to a gallery is intentionally a separate step. A course video is
not pushed to the cloud until the operator explicitly does so.
