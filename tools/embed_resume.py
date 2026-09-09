#!/usr/bin/env python3
"""Embed a PDF byte-for-byte for the site's client-side résumé download."""

from __future__ import annotations

import argparse
import base64
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output", type=Path, default=Path("assets/resume-data.js"))
    args = parser.parse_args()

    encoded = base64.b64encode(args.pdf.read_bytes()).decode("ascii")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        f'window.YIBO_RESUME_BASE64="{encoded}";\n',
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
