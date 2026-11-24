"""Stdlib-only tests for the portable tiny-voca CLI and receipt chain.

No network, no numpy/onnxruntime/dizione: synthesis and heavy modules are
mocked with tiny in-process fakes.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import py_compile
import struct
import sys
import tempfile
import unittest
import wave
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import tiny_voca_paths as paths  # noqa: E402
import tiny_voca_verify as verify  # noqa: E402
import tiny_voca_voice as voice  # noqa: E402


class FakeArray(list):
    """Just enough numpy.ndarray behaviour for the synthesis path."""

    def __init__(self, values=(), dtype=None):
        super().__init__(values)
        self.dtype = dtype

    @property
    def size(self):
        return len(self)

    def __mul__(self, scalar):
        return FakeArray([value * scalar for value in self], self.dtype)

    __rmul__ = __mul__

    def __abs__(self):
        return FakeArray([abs(value) for value in self], self.dtype)

    def max(self):
        return max(self) if len(self) else 0.0

    def astype(self, dtype):
        if dtype == "<i2":
            return FakeArray([int(float(value)) for value in self], dtype)
        return FakeArray([float(value) for value in self], dtype)

    def tobytes(self):
        return struct.pack("<%dh" % len(self), *[int(value) for value in self])


class FakeNumpy:
    float32 = "float32"
    int64 = "int64"

    def zeros(self, count, dtype=None):
        return FakeArray([0.0] * int(count), dtype)

    def array(self, values, dtype=None):
        return FakeArray(list(values), dtype)

    def concatenate(self, arrays):
        joined = FakeArray([], getattr(arrays[0], "dtype", None) if arrays else None)
        for array in arrays:
            joined.extend(array)
        return joined

    def clip(self, array, low, high):
        return FakeArray([max(low, min(high, float(value))) for value in array],
                         getattr(array, "dtype", None))

    def abs(self, array):
        return abs(array)


def fake_result(output="out.wav", duration_s=1.234, sha256="abc"):
    return {"success": True, "output": output, "sentences": 1,
            "duration_s": duration_s, "sample_rate": paths.SAMPLE_RATE,
            "sha256": sha256}


class PathAliasTests(unittest.TestCase):
    def test_runtime_root_prefers_TINY_VOCA_HOME(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(
            os.environ, {"TINY_VOCA_HOME": tmp, "HERMES_HOME": tmp + "/other"}, clear=False
        ):
            self.assertEqual(paths.runtime_root(), Path(tmp))
            self.assertEqual(paths.model_path(), Path(tmp) / "onnx" / "model.onnx")
            self.assertEqual(paths.config_path(), Path(tmp) / "config.json")
            self.assertEqual(paths.phonemizer_dir(), Path(tmp) / "phonemizer")
            self.assertEqual(paths.apply_env(), str(Path(tmp) / "phonemizer"))
            self.assertEqual(os.environ["DIZIONE_DATA"], str(Path(tmp) / "phonemizer"))

    def test_runtime_root_falls_back_to_HERMES_HOME(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(
            os.environ, {"HERMES_HOME": tmp}, clear=False
        ):
            os.environ.pop("TINY_VOCA_HOME", None)
            self.assertEqual(paths.runtime_root(), Path(tmp) / "tiny-voca")
            self.assertEqual(paths.model_path(), Path(tmp) / "tiny-voca" / "onnx" / "model.onnx")

    def test_ledger_and_output_defaults(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("HERMES_TINY_VOCA_LEDGER", None)
            os.environ["HERMES_HOME"] = tmp
            self.assertEqual(paths.ledger_path(), Path(tmp) / "tiny-voca-receipts.jsonl")
            os.environ["HERMES_TINY_VOCA_LEDGER"] = str(Path(tmp) / "custom.jsonl")
            self.assertEqual(paths.ledger_path(), Path(tmp) / "custom.jsonl")
            self.assertEqual(paths.default_output(), Path.home() / ".hermes" / "tiny-voca-out.wav")

    def test_all_voice_aliases_canonicalize(self):
        expected = {
            "F2": ["F2", "f2", "nous-girl", "nous_girl", "nous girl", "  Nous   Girl "],
            "M2": ["M2", "m2", "hermes-agent", "hermes_agent", "hermes agent", "HERMES_AGENT"],
        }
        for canonical, aliases in expected.items():
            for alias in aliases:
                with self.subTest(alias=alias):
                    self.assertEqual(paths.canonical_voice(alias), canonical)
        with self.assertRaises(ValueError):
            paths.canonical_voice("third-voice")


class SynthesisTests(unittest.TestCase):
    def test_split_sentences_keeps_punctuation_and_chunks(self):
        text = "First one!  Second two?  Third three.  " + ("word " * 80)
        sentences = voice.split_sentences(text, limit=60)
        self.assertGreater(len(sentences), 3)
        self.assertTrue(all(sentence[-1] in ".!?" for sentence in sentences[:3]))
        self.assertTrue(all(len(sentence) <= 61 for sentence in sentences))
        self.assertEqual(voice.split_sentences("   "), [])

    def test_synthesize_normalizes_peak_and_sets_env(self):
        class Phones:
            ids = [1, 2, 3]
            stress = [0, 1, 0]

        class Dizione:
            @staticmethod
            def phonemize(text):
                return Phones()

        calls = []

        class Session:
            def run(self, fetches, feeds):
                calls.append({"feeds": feeds})
                return [FakeArray([2.0, -2.0, 1.0])], None

        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(
            os.environ, {"TINY_VOCA_HOME": tmp}, clear=False
        ), mock.patch.dict(sys.modules, {"dizione": Dizione}), mock.patch.object(
            voice, "_numpy", return_value=FakeNumpy()
        ), mock.patch.object(voice, "session", return_value=Session()):
            result = voice.synthesize("Hello there.", "nous girl", speed=1.2)
            self.assertLessEqual(result.max(), 0.99 + 1e-9)
            self.assertAlmostEqual(result.max(), 0.99, places=6)
            self.assertEqual(os.environ["DIZIONE_DATA"], str(Path(tmp) / "phonemizer"))
            self.assertEqual(list(calls[0]["feeds"]["voice"]), [0])
            self.assertEqual(list(calls[0]["feeds"]["speed"]), [1.2])

    def test_speak_text_writes_24000_hz_mono_wav_with_180ms_gaps(self):
        chunk_a = FakeArray([0.5, -0.5, 0.25])
        chunk_b = FakeArray([0.1, -0.1])

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "nested" / "speech.wav"
            with mock.patch.object(voice, "_numpy", return_value=FakeNumpy()), mock.patch.object(
                voice, "synthesize", side_effect=[chunk_a, chunk_b]
            ) as synthesize:
                result = voice.speak_text("One. Two.", str(output), "hermes-agent")
            self.assertEqual(synthesize.call_count, 2)
            self.assertEqual(synthesize.call_args_list[0].args[1], "M2")
            with wave.open(str(output), "rb") as handle:
                self.assertEqual(handle.getnchannels(), 1)
                self.assertEqual(handle.getsampwidth(), 2)
                self.assertEqual(handle.getframerate(), paths.SAMPLE_RATE)
                frames = handle.readframes(handle.getnframes())
            expected_samples = len(chunk_a) + int(paths.SAMPLE_RATE * 0.18) + len(chunk_b)
            self.assertEqual(len(frames) // 2, expected_samples)
            self.assertTrue(result["success"])
            self.assertEqual(result["voice"], "M2")
            self.assertEqual(result["sentences"], 2)
            self.assertEqual(result["duration_s"], round(expected_samples / paths.SAMPLE_RATE, 3))
            self.assertEqual(result["sha256"], __import__("hashlib").sha256(output.read_bytes()).hexdigest())


class CLITests(unittest.TestCase):
    def _main(self, argv):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            code = voice.main(argv)
        lines = [line for line in stream.getvalue().splitlines() if line.strip()]
        self.assertEqual(len(lines), 1, lines)
        return code, json.loads(lines[0])

    def test_voice_alias_and_receipt_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "receipts.jsonl"
            env = {"HERMES_TINY_VOCA_LEDGER": str(ledger),
                   "TINY_VOCA_HOME": str(Path(tmp) / "runtime")}
            result = fake_result(output=str(Path(tmp) / "one.wav"), sha256="a" * 64)
            with mock.patch.dict(os.environ, env, clear=False), mock.patch.object(
                voice, "speak_text", return_value=result
            ) as speak:
                code, first = self._main(["--text", "Hello.", "--voice", "nous girl",
                                          "--output", result["output"]])
                self.assertEqual(code, 0)
                self.assertEqual(speak.call_args.args[2], "F2")
            self.assertTrue(first["success"])
            self.assertEqual(first["voice"], "F2")
            self.assertEqual(first["alias"], "nous girl")
            receipt = first["receipt"]
            self.assertEqual(receipt["action"], "TTS://SPEAK")
            self.assertEqual(receipt["authority"], "HUMAN://ROOT")
            self.assertEqual(receipt["voice"], "F2")
            self.assertEqual(receipt["alias"], "nous girl")
            self.assertEqual(receipt["success"], True)
            self.assertEqual(receipt["sha256"], "a" * 64)
            self.assertEqual(receipt["prev"], paths.GENESIS)
            self.assertEqual(receipt["hash"], paths.compute_hash(receipt["prev"], receipt))
            self.assertEqual(set(receipt), {"ts", "action", "authority", "voice", "alias",
                                            "success", "sha256", "duration_s", "output",
                                            "prev", "hash"})

            second_result = fake_result(output=str(Path(tmp) / "two.wav"), sha256="b" * 64)
            with mock.patch.dict(os.environ, env, clear=False), mock.patch.object(
                voice, "speak_text", return_value=second_result
            ) as speak:
                code, second = self._main(["--text", "Bye.", "--voice", "hermes agent",
                                           "--output", second_result["output"]])
                self.assertEqual(code, 0)
                self.assertEqual(speak.call_args.args[2], "M2")
            self.assertEqual(second["voice"], "M2")
            self.assertEqual(second["receipt"]["prev"], receipt["hash"])
            self.assertEqual(second["receipt"]["voice"], "M2")
            chain = paths.verify_chain(ledger)
            self.assertTrue(chain["ok"])
            self.assertEqual(chain["count"], 2)
            self.assertEqual(chain["head"], second["receipt"]["hash"])

    def test_text_file_takes_precedence_and_receipt_failure_is_nonfatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            text_file = Path(tmp) / "prompt.txt"
            text_file.write_text("FromFile.", encoding="utf-8")
            result = fake_result(output=str(Path(tmp) / "out.wav"))
            with tempfile.TemporaryDirectory() as ledger_dir, mock.patch.dict(
                os.environ, {"HERMES_TINY_VOCA_LEDGER": str(Path(ledger_dir) / "r.jsonl")},
                clear=False
            ), mock.patch.object(voice, "speak_text", return_value=result) as speak, mock.patch.object(
                paths, "append_receipt", side_effect=OSError("ledger is read-only")
            ):
                code, payload = self._main(["--text", "ignored", "--text-file", str(text_file)])
            self.assertEqual(code, 0)
            self.assertTrue(payload["success"])
            self.assertIsNone(payload["receipt"])
            self.assertIn("ledger is read-only", payload["receipt_error"])
            self.assertEqual(speak.call_args.args[0], "FromFile.")

    def test_invalid_input_returns_json_error(self):
        code, payload = self._main([])
        self.assertEqual(code, 1)
        self.assertFalse(payload["success"])
        self.assertIn("text", payload["error"])
        code, payload = self._main(["--text", "Hello.", "--voice", "unknown"])
        self.assertEqual(code, 1)
        self.assertFalse(payload["success"])


class VerifyTests(unittest.TestCase):
    def test_verify_script_detects_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "receipts.jsonl"
            entries = []
            prev = paths.GENESIS
            for index in range(2):
                entry = {"ts": "2026-01-01T00:00:00Z", "action": paths.ACTION_TTS_SPEAK,
                         "authority": paths.AUTHORITY, "voice": "F2", "alias": "F2",
                         "success": True, "sha256": str(index) * 64, "duration_s": 1.0,
                         "output": "out.wav", "prev": prev}
                entry["hash"] = paths.compute_hash(prev, entry)
                entries.append(entry)
                prev = entry["hash"]
            ledger.write_text("\n".join(json.dumps(e) for e in entries) + "\n", encoding="utf-8")
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                code = verify.main(["--ledger", str(ledger)])
            self.assertEqual(code, 0)
            report = json.loads(stream.getvalue().strip())
            self.assertTrue(report["ok"])
            self.assertEqual(report["count"], 2)

            tampered = [dict(entries[0]), entries[1]]
            tampered[0]["duration_s"] = 999.0
            ledger.write_text("\n".join(json.dumps(e) for e in tampered) + "\n", encoding="utf-8")
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                code = verify.main(["--ledger", str(ledger)])
            self.assertEqual(code, 1)
            report = json.loads(stream.getvalue().strip())
            self.assertFalse(report["ok"])
            self.assertEqual(report["broken_at"], 1)


class PluginDelegationTests(unittest.TestCase):
    def test_handlers_delegate_to_scripts_via_mocked_subprocess(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("tiny_voca_cli_plugin", REPO / "__init__.py")
        plugin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin)

        tools = {}

        class Ctx:
            def register_tool(self, name, toolset, handler, schema):
                tools[name] = handler

            def register_skill(self, name, path):
                pass

        plugin.register(Ctx())
        payload = {"success": True, "voice": "M2", "sha256": "c" * 64}
        completed = mock.Mock(returncode=0, stdout=json.dumps(payload) + "\n", stderr="")
        with mock.patch.object(plugin.subprocess, "run", return_value=completed) as run:
            spoken = json.loads(tools["tts_speak"]({"text": "Hi.", "voice": "nous-girl"}))
            command = run.call_args.args[0]
        self.assertTrue(spoken["success"])
        self.assertEqual(spoken["voice"], "M2")
        self.assertIn("tiny_voca_voice.py", command[1])
        self.assertIn("nous-girl", command)

        with mock.patch.object(plugin.subprocess, "run", return_value=completed) as run:
            tools["tts_verify"]({})
        self.assertIn("tiny_voca_verify.py", run.call_args.args[0][1])


class PortabilityTests(unittest.TestCase):
    def test_scripts_compile_without_heavy_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("tiny_voca_paths.py", "tiny_voca_voice.py", "tiny_voca_verify.py"):
                py_compile.compile(str(SCRIPTS / name), cfile=str(Path(tmp) / (name + "c")),
                                   doraise=True)

    def test_no_machine_local_root_in_committed_code(self):
        needle = "/opt" + "/data"
        files = [SCRIPTS / name for name in
                 ("tiny_voca_paths.py", "tiny_voca_voice.py", "tiny_voca_verify.py")]
        files += [REPO / "__init__.py", REPO / "plugin.yaml", REPO / "pyproject.toml",
                  REPO / "skills" / "tiny-voca-voice" / "SKILL.md"]
        for path in files:
            self.assertNotIn(needle, path.read_text(encoding="utf-8"), str(path))


if __name__ == "__main__":
    unittest.main()
