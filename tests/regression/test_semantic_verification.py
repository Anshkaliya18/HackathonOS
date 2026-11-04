#!/usr/bin/env python3
"""Adversarial regression tests for the semantic verification system.

Tests the compatibility gates and decision logic against tricky cases:
1. paraphrased supported claim
2. exact supported claim
3. semantically similar but unsupported claim
4. numerical mismatch
5. entity mismatch
6. polarity mismatch
7. temporal mismatch
8. partial claim
9. contradictory evidence
10. irrelevant semantic evidence
11. multi-document support
12. no evidence
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from verification import (  # noqa: E402
    verify_claim,
    SUPPORTED,
    PARTIALLY_SUPPORTED,
    UNSUPPORTED,
    CONTRADICTED,
)

VALID_LABELS = {SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONTRADICTED}

failures: list[str] = []


def check(label: str, claim: str, evidence: str, expected: str) -> None:
    result = verify_claim(claim, evidence)
    pred = result.label
    ok = pred == expected
    status = "PASS" if ok else "FAIL"
    if not ok:
        failures.append(
            f"{label}: claim='{claim}' evidence='{evidence}' "
            f"expected={expected} got={pred} sim={result.semantic_similarity} "
            f"cov={result.coverage} conf={result.confidence}"
        )
    print(f"  [{status}] {label}: expected={expected} got={pred} sim={result.semantic_similarity:.3f}")


def main() -> int:
    print("=== Adversarial regression tests for semantic verification ===\n")

    # 1. Paraphrased supported claim
    check(
        "paraphrased supported",
        "sherpa uses JSON for configuration.",
        "sherpa uses JSON configuration files (manifest.json, settings.json).",
        SUPPORTED,
    )

    # 2. Exact supported claim
    check(
        "exact supported",
        "sherpa is written in Python.",
        "sherpa configuration manager is written in Python.",
        SUPPORTED,
    )

    # 3. Semantically similar but unsupported (different subject)
    check(
        "semantically similar unsupported",
        "sherpa uses Python.",
        "The weather is sunny today in California.",
        UNSUPPORTED,
    )

    # 4. Numerical mismatch
    check(
        "numerical mismatch",
        "sherpa has 15 lifecycle phases.",
        "Lifecycle has exactly 20 phases.",
        CONTRADICTED,
    )

    # 5. Entity mismatch (different subject with high similarity)
    check(
        "entity mismatch",
        "System A uses Python for processing.",
        "System B uses Python for processing.",
        UNSUPPORTED,
    )

    # 6. Polarity mismatch
    check(
        "polarity mismatch",
        "sherpa does not require human approval.",
        "REQUIRE_HUMAN_APPROVAL=true.",
        CONTRADICTED,
    )

    # 7. Temporal mismatch
    check(
        "temporal mismatch",
        "sherpa was created in 2025.",
        "Repository files show LastWriteTime 31-10-2026.",
        CONTRADICTED,
    )

    # 8. Partial claim (one element supported, one not)
    check(
        "partial claim",
        "sherpa uses Python and is deployed on AWS.",
        "sherpa configuration manager is written in Python.",
        PARTIALLY_SUPPORTED,
    )

    # 9. Contradictory evidence
    check(
        "contradictory evidence",
        "sherpa verification is disabled.",
        "verification: { enabled: true }. ENABLE_AUTO_VERIFY=true.",
        CONTRADICTED,
    )

    # 10. Irrelevant semantic evidence (high word overlap, no support)
    check(
        "irrelevant semantic evidence",
        "sherpa reduces development time by 50%.",
        "sherpa top-level directories: adapters, commands, core, docs.",
        UNSUPPORTED,
    )

    # 11. Multi-document support (evidence text combines both docs)
    check(
        "multi-document support",
        "sherpa uses Python and has verification enabled.",
        "sherpa configuration manager is written in Python. verification: { enabled: true }.",
        SUPPORTED,
    )

    # 12. No evidence (empty evidence)
    check(
        "no evidence",
        "sherpa has a mobile app.",
        "",
        UNSUPPORTED,
    )

    # 13. Empty claim
    check(
        "empty claim",
        "",
        "sherpa uses Python.",
        UNSUPPORTED,
    )

    # 14. Compound claim fully supported
    check(
        "compound fully supported",
        "sherpa uses Python and requires human approval.",
        "sherpa configuration manager is written in Python. REQUIRE_HUMAN_APPROVAL=true.",
        SUPPORTED,
    )

    # 15. Negation match (both negated)
    check(
        "negation match",
        "sherpa does not use Python.",
        "sherpa does not use Python.",
        SUPPORTED,
    )

    # 16. Supported with strong semantic match (paraphrase)
    check(
        "strong paraphrase supported",
        "The system has twelve components.",
        "The system explicitly contains twelve components in its architecture.",
        SUPPORTED,
    )

    # 17. Contradicted with different number same magnitude
    check(
        "contradicted different number",
        "Maximum auto iterations is 5.",
        "MAX_AUTO_ITERATIONS=10.",
        CONTRADICTED,
    )

    # 18. Supported exact match
    check(
        "supported exact match",
        "master_command: /sherpa.",
        "master_command: /sherpa.",
        SUPPORTED,
    )

    print()
    if failures:
        print(f"ADVERSARIAL TESTS: {len(failures)} FAILURE(S)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"ADVERSARIAL TESTS: ALL PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
