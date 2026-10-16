import asyncio
import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import qrcode
from PIL import Image
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from aeqr_vision_mcp import server


class VisionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "approved"
        self.root.mkdir()
        self.scope = patch.object(server, "IMAGE_ROOT", self.root)
        self.scope.start()
        qrcode.make("https://example.test/resource").save(self.root / "qr.png")

    def tearDown(self):
        self.scope.stop()
        self.tmp.cleanup()

    def test_decode_and_evidence(self):
        result = server.scan_qr("qr.png")
        self.assertEqual(result["observation"]["codes"][0]["payload"],
                         "https://example.test/resource")
        self.assertEqual(result["evidence"]["source_sha256"],
                         hashlib.sha256((self.root / "qr.png").read_bytes()).hexdigest())
        self.assertFalse(result["authority_granted"])
        self.assertFalse(result["observation"]["urls_opened"])

    def test_traversal_and_symlink_escape(self):
        outside = Path(self.tmp.name) / "outside.png"
        Image.new("RGB", (20, 20), "white").save(outside)
        with self.assertRaises(ValueError):
            server.scan_qr("../outside.png")
        (self.root / "link.png").symlink_to(outside)
        with self.assertRaises(ValueError):
            server.scan_qr("link.png")
        with self.assertRaises(ValueError):
            server.scan_qr(str(outside))

    def test_blank_and_limits(self):
        Image.new("RGB", (20, 20), "white").save(self.root / "blank.png")
        self.assertTrue(server.scan_qr("blank.png")["observation"]["no_code_found"])
        with patch.object(server, "MAX_BYTES", 10):
            with self.assertRaises(ValueError):
                server.scan_qr("qr.png")
        with patch.object(server, "MAX_PIXELS", 10):
            with self.assertRaises(ValueError):
                server.scan_qr("qr.png")

    def test_stdio_protocol(self):
        async def exercise():
            params = StdioServerParameters(command=sys.executable,
                args=["-m", "aeqr_vision_mcp.server"],
                env={**os.environ, "AEQR_VISION_IMAGE_ROOT": str(self.root)})
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as client:
                    await client.initialize()
                    tools = (await client.list_tools()).tools
                    self.assertEqual({t.name for t in tools},
                        {"vision_status", "scan_qr", "calibration_reference"})
                    for tool in tools:
                        self.assertTrue(tool.annotations.readOnlyHint)
                    for name, args in [("vision_status", {}),
                            ("calibration_reference", {}),
                            ("scan_qr", {"image_path": "qr.png"})]:
                        result = await client.call_tool(name, args)
                        self.assertFalse(result.isError, result.content)
                    result = await client.call_tool("scan_qr",
                        {"image_path": "../outside.png"})
                    self.assertTrue(result.isError)
        # The rejected path may be nonexistent here; either error must stay closed.
        asyncio.run(exercise())


if __name__ == "__main__":
    unittest.main()
