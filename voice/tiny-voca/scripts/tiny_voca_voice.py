#!/usr/bin/env python3
"""Portable tiny-voca CLI: English TTS with hash-chained HUMAN://ROOT receipts.

Runtime deps (numpy, onnxruntime, dizione) are imported lazily inside the
synthesis path so this file can be byte-compiled and unit-tested without them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import wave
from pathlib import Path

import tiny_voca_paths as paths

SR = paths.SAMPLE_RATE
VOICE_IDS = {"F2": 0, "M2": 1}
_session = None


def _numpy():
    """Lazy numpy import — only called on the actual synthesis path."""
    import numpy as np
    return np


def session():
    """Lazily create the ONNX Runtime CPU session for the resolved model."""
    global _session
    if _session is None:
        import onnxruntime as ort
        model = paths.model_path()
        if not model.exists():
            raise FileNotFoundError("tiny-voca model not found: %s" % model)
        options = ort.SessionOptions()
        options.intra_op_num_threads = 4
        options.log_severity_level = 3
        _session = ort.InferenceSession(str(model), options,
                                        providers=["CPUExecutionProvider"])
    return _session


def split_sentences(text, limit=300):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    out = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part[-1] not in ".!?":
            part += "."
        while len(part) > limit:
            cut = part.rfind(" ", 0, limit)
            if cut < 0:
                cut = limit
            out.append(part[:cut + 1].strip())
            part = part[cut + 1:].strip()
        if part:
            out.append(part)
    return out


def synthesize(text, voice="F2", speed=1.0, pitch_shift=0.0, pitch_range=1.0):
    """text -> float32 waveform at 24 kHz (one utterance, <=512 tokens)."""
    canonical = paths.canonical_voice(voice)
    np = _numpy()
    paths.apply_env()
    import dizione
    phones = dizione.phonemize(text)
    if not phones or not getattr(phones, "ids", None):
        raise ValueError("nothing in the text could be read: tiny-voca only reads English for now")
    one = lambda value: np.array([value], dtype=np.float32)
    audio, _ = session().run(None, {
        "tokens": np.array([phones.ids], dtype=np.int64),
        "stress": np.array([phones.stress], dtype=np.int64),
        "voice": np.array([VOICE_IDS[canonical]], dtype=np.int64),
        "speed": one(speed),
        "pitch_shift": one(pitch_shift),
        "pitch_range": one(pitch_range),
    })
    waveform = audio[0].astype(np.float32)
    peak = float(np.abs(waveform).max()) if waveform.size else 0.0
    if peak > 0.99:
        waveform = waveform * (0.99 / peak)
    return waveform


def speak_text(text, output, voice="F2", speed=1.0, pitch_shift=0.0, pitch_range=1.0):
    """Long text -> single 16-bit WAV; joins sentences with 180 ms silence."""
    np = _numpy()
    canonical = paths.canonical_voice(voice)
    sentences = split_sentences(text)
    if not sentences:
        raise ValueError("nothing in the text could be read")
    chunks = [synthesize(sentence, canonical, speed, pitch_shift, pitch_range)
              for sentence in sentences]
    gap = np.zeros(int(SR * 0.18), dtype=np.float32)
    joined = np.concatenate(
        [chunk for index, chunk in enumerate(chunks)
         for chunk in ([gap] if index else []) + [chunk]]
    )
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    pcm = (np.clip(joined, -1.0, 1.0) * 32767).astype("<i2")
    with wave.open(str(destination), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(SR)
        handle.writeframes(pcm.tobytes())
    return {
        "success": True,
        "output": str(destination),
        "voice": canonical,
        "sentences": len(sentences),
        "duration_s": round(len(joined) / SR, 3),
        "sample_rate": SR,
        "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="tiny-voca local TTS (ONNX)")
    parser.add_argument("--text", default=None)
    parser.add_argument("--text-file", default=None,
                        help="Read text from a UTF-8 file (Hermes TTS convention).")
    parser.add_argument("--voice", default="M2",
                        help="F2/nous-girl or M2/hermes-agent (aliases accepted).")
    parser.add_argument("--output", default=None)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--pitch-shift", type=float, default=0.0)
    parser.add_argument("--pitch-range", type=float, default=1.0)
    args = parser.parse_args(argv)

    try:
        canonical = paths.canonical_voice(args.voice)
    except ValueError as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    if args.text_file:
        try:
            text = Path(args.text_file).expanduser().read_text(encoding="utf-8")
        except OSError as exc:
            print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False))
            return 1
    elif args.text:
        text = args.text
    else:
        print(json.dumps({"success": False, "error": "text or --text-file is required"},
                         ensure_ascii=False))
        return 1

    output = args.output or str(paths.default_output())
    paths.apply_env()
    try:
        result = speak_text(text, output, canonical, args.speed,
                            args.pitch_shift, args.pitch_range)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    result["voice"] = canonical
    result["alias"] = args.voice
    try:
        result["receipt"] = paths.append_receipt(
            result, canonical, args.voice, paths.ledger_path())
    except Exception as exc:  # a receipt failure must never break synthesis
        result["receipt"] = None
        result["receipt_error"] = str(exc)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
