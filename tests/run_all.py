"""Run Sherpa's test suites in ordered, selectable phases."""

import argparse
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST_ROOT = ROOT / "tests"
PHASES = {
    "smoke": ("smoke",),
    "core": ("commands", "configuration", "ideas"),
    "workflows": ("workflows",),
    "regression": ("regression",),
    "distribution": ("installer",),
}


def files_for_phase(phase: str) -> list[Path]:
    folders = PHASES[phase]
    return sorted(
        path
        for folder in folders
        for path in (TEST_ROOT / folder).rglob("test_*.py")
        if path.name != "__init__.py"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--phase",
        choices=("all", *PHASES),
        default="all",
        help="run one test phase, or all phases in order (default: all)",
    )
    args = parser.parse_args()

    phases = list(PHASES) if args.phase == "all" else [args.phase]
    failures = []
    total = 0
    for phase in phases:
        files = files_for_phase(phase)
        total += len(files)
        print(f"\n=== Phase {list(PHASES).index(phase) + 1}: {phase} ({len(files)} files) ===")

        if phase == "distribution":
            command = [sys.executable, "-m", "pytest", "tests/installer", "-q"]
            label = Path("tests/installer")
            start = time.monotonic()
            try:
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=300, check=False)
            except subprocess.TimeoutExpired as error:
                failures.append((label, f"timed out after {error.timeout}s"))
                print(f"FAIL {label}: timed out")
                continue
            elapsed = time.monotonic() - start
            if result.returncode:
                details = (result.stdout + "\n" + result.stderr).strip()
                failures.append((label, details[-4000:]))
                print(f"FAIL {label} ({elapsed:.1f}s)")
                if details:
                    print(details[-4000:])
            else:
                print(f"PASS {label} ({elapsed:.1f}s)")
            continue

        for test_file in files:
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
        print(f"\n{len(failures)} test phase(s) or file(s) failed:")
        for file, details in failures:
            print(f"\n--- {file} ---\n{details}")
        return 1

    print(f"\nAll selected phases passed ({total} test files discovered).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
