#!/usr/bin/env python3
"""Verify the tiny-voca receipt hash chain. Prints one JSON line."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import tiny_voca_paths as paths


def main(argv=None):
    parser = argparse.ArgumentParser(description="verify tiny-voca TTS://SPEAK receipts")
    parser.add_argument("--ledger", default=None,
                        help="Receipt JSONL (default: resolved ledger path).")
    args = parser.parse_args(argv)
    ledger = Path(args.ledger).expanduser() if args.ledger else paths.ledger_path()
    report = paths.verify_chain(ledger)
    report["ledger"] = str(ledger)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
