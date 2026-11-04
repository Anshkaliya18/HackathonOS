"""Run each self-contained Python test suite in isolation."""

import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST_ROOT = ROOT / "tests"
FILES = sorted(
    path
    for path in TEST_ROOT.rglob("test_*.py")
    if path.name != "__init__.py"
)


def main() -> int:
    failures = []
    for test_file in FILES:
        relative = test_file.relative_to(ROOT)
        start = time.monotonic()
        try:
            result = subprocess.run(
                [sys.executable, str(test_file)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            failures.append((relative, f"timed out after {error.timeout}s"))
            print(f"FAIL {relative}: timed out")
            continue

        elapsed = time.monotonic() - start
        if result.returncode:
            details = (result.stdout + "\n" + result.stderr).strip()
            failures.append((relative, details[-4000:]))
            print(f"FAIL {relative} ({elapsed:.1f}s)")
        else:
            print(f"PASS {relative} ({elapsed:.1f}s)")

    if failures:
        print(f"\n{len(failures)} of {len(FILES)} test files failed:")
        for file, details in failures:
            print(f"\n--- {file} ---\n{details}")
        return 1

    print(f"\nAll {len(FILES)} Python test files passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
