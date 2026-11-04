#!/usr/bin/env python3
"""Extract one version's release notes from CHANGELOG.md."""

import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: release-notes.py <tag> <output-file>", file=sys.stderr)
        return 2

    tag = sys.argv[1]
    match = re.fullmatch(r"v?(\d+\.\d+\.\d+)", tag)
    if not match:
        print(f"tag must be a semantic version such as v1.2.3: {tag}", file=sys.stderr)
        return 2

    version = match.group(1)
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    lines = changelog.splitlines()
    heading = re.compile(rf"^##\s+\[?{re.escape(version)}\]?(?:\s|$)")
    start = next((i for i, line in enumerate(lines) if heading.match(line)), None)
    if start is None:
        print(f"CHANGELOG.md has no release section for {version}.", file=sys.stderr)
        return 1

    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    notes = "\n".join(lines[start + 1 : end]).strip()
    if not notes:
        print(f"CHANGELOG.md release section for {version} is empty.", file=sys.stderr)
        return 1

    Path(sys.argv[2]).write_text(notes + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
