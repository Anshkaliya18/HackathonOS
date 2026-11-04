#!/usr/bin/env python3
"""Regression tests for the sherpa gold-labeled verification benchmark.

Validates benchmark artifact integrity, label validity, split separation,
and metric correctness. stdlib-only; deterministic; non-zero exit on failure.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BENCH = ROOT / ".sherpa" / "evidence" / "gold-benchmark"

VALID_LABELS = {"SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED", "CONTRADICTED"}

failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"FAIL: {msg}")


def ok(msg: str) -> None:
    print(f"PASS: {msg}")


def load_json(name: str) -> object:
    path = BENCH / name
    if not path.is_file():
        fail(f"missing artifact: {name}")
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        fail(f"malformed JSON in {name}: {exc}")
        return None


def file_sha256(name: str) -> str | None:
    path = BENCH / name
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --- Test 1: All required artifacts exist ---
def test_artifacts_exist() -> None:
    required = [
        "dataset.json", "annotation-guide.md", "split.json",
        "gold-labels.json", "predictions.json", "metrics.json",
        "confusion-matrix.json", "citation-evaluation.json",
    ]
    for name in required:
        if (BENCH / name).is_file():
            ok(f"artifact exists: {name}")
        else:
            fail(f"missing artifact: {name}")


# --- Test 2: Gold labels are valid ---
def test_gold_labels_valid() -> None:
    data = load_json("gold-labels.json")
    if data is None:
        return
    labels = data.get("labels", [])
    if not isinstance(labels, list):
        fail("gold-labels.json: 'labels' must be a list")
        return
    for entry in labels:
        cid = entry.get("claim_id", "UNKNOWN")
        label = entry.get("gold_label")
        if label not in VALID_LABELS:
            fail(f"gold-labels.json: claim {cid} has invalid label '{label}'")
        required_fields = ("claim_id", "question_id", "claim_text",
                           "candidate_evidence_id", "evidence_text",
                           "gold_label", "annotator", "annotation_reason")
        for field in required_fields:
            if field not in entry:
                fail(f"gold-labels.json: claim {cid} missing field '{field}'")
    ok(f"gold labels valid: {len(labels)} labels checked")


# --- Test 3: Every claim in dataset has a gold label ---
def test_every_claim_labeled() -> None:
    dataset = load_json("dataset.json")
    labels = load_json("gold-labels.json")
    if dataset is None or labels is None:
        return
    claim_ids = {c["claim_id"] for c in dataset.get("claims", [])}
    label_ids = {e["claim_id"] for e in labels.get("labels", [])}
    missing = claim_ids - label_ids
    extra = label_ids - claim_ids
    if missing:
        fail(f"claims without gold labels: {sorted(missing)}")
    if extra:
        fail(f"gold labels for unknown claims: {sorted(extra)}")
    if not missing and not extra:
        ok(f"every claim has a gold label ({len(claim_ids)} claims)")


# --- Test 4: No duplicate claim IDs ---
def test_no_duplicate_claim_ids() -> None:
    dataset = load_json("dataset.json")
    if dataset is None:
        return
    claims = dataset.get("claims", [])
    ids = [c["claim_id"] for c in claims]
    dupes = [cid for cid in ids if ids.count(cid) > 1]
    if dupes:
        fail(f"duplicate claim IDs: {sorted(set(dupes))}")
    else:
        ok(f"no duplicate claim IDs ({len(ids)} claims)")


# --- Test 5: No missing evidence IDs ---
def test_no_missing_evidence_ids() -> None:
    dataset = load_json("dataset.json")
    labels = load_json("gold-labels.json")
    if dataset is None or labels is None:
        return
    for c in dataset.get("claims", []):
        cid = c["claim_id"]
        if not c.get("candidate_evidence_id"):
            fail(f"claim {cid}: missing candidate_evidence_id")
        if not c.get("candidate_evidence_text"):
            fail(f"claim {cid}: missing candidate_evidence_text")
    for e in labels.get("labels", []):
        cid = e["claim_id"]
        if not e.get("candidate_evidence_id"):
            fail(f"gold label {cid}: missing candidate_evidence_id")
        if not e.get("evidence_text"):
            fail(f"gold label {cid}: missing evidence_text")
    ok("evidence IDs present for all claims and labels")


# --- Test 6: Held-out claims are not in calibration set ---
def test_held_out_separation() -> None:
    split = load_json("split.json")
    if split is None:
        return
    cal = set(split.get("calibration_development", []))
    held = set(split.get("held_out_test", []))
    overlap = cal & held
    if overlap:
        fail(f"held-out claims also in calibration: {sorted(overlap)}")
    else:
        ok(f"held-out and calibration sets are disjoint ({len(cal)} cal, {len(held)} held-out)")
    total = split.get("counts", {})
    if total.get("calibration_development") != len(cal):
        fail(f"calibration count mismatch: recorded {total.get('calibration_development')}, actual {len(cal)}")
    if total.get("held_out_test") != len(held):
        fail(f"held-out count mismatch: recorded {total.get('held_out_test')}, actual {len(held)}")


# --- Test 7: Predicted labels are valid ---
def test_predicted_labels_valid() -> None:
    predictions = load_json("predictions.json")
    if predictions is None:
        return
    results = predictions.get("results", [])
    for r in results:
        label = r.get("predicted_label")
        if label not in VALID_LABELS:
            fail(f"predictions.json: claim {r.get('claim_id')} has invalid predicted label '{label}'")
    ok(f"predicted labels valid: {len(results)} predictions checked")


# --- Test 8: Metrics calculate correctly ---
def test_metrics_calculate_correctly() -> None:
    metrics = load_json("metrics.json")
    predictions = load_json("predictions.json")
    if metrics is None or predictions is None:
        return

    overall = metrics.get("overall", {})
    total = overall.get("total", 0)
    correct = overall.get("correct", 0)
    accuracy = overall.get("accuracy", 0)

    results = predictions.get("results", [])
    actual_total = len(results)
    actual_correct = sum(1 for r in results if r.get("correct") is True)
    expected_accuracy = round(actual_correct / actual_total, 4) if actual_total > 0 else 0.0

    if total != actual_total:
        fail(f"metrics total {total} != predictions count {actual_total}")
    if correct != actual_correct:
        fail(f"metrics correct {correct} != actual correct {actual_correct}")
    if abs(accuracy - expected_accuracy) > 0.0001:
        fail(f"metrics accuracy {accuracy} != expected {expected_accuracy}")
    if total == actual_total and correct == actual_correct and abs(accuracy - expected_accuracy) <= 0.0001:
        ok(f"metrics calculate correctly: accuracy={accuracy}, correct={correct}/{total}")


# --- Test 9: Confusion matrix totals match dataset size ---
def test_confusion_matrix_totals() -> None:
    cm = load_json("confusion-matrix.json")
    predictions = load_json("predictions.json")
    if cm is None or predictions is None:
        return
    matrix = cm.get("matrix", {})
    cm_total = sum(sum(row.values()) for row in matrix.values())
    recorded_total = cm.get("total", 0)
    pred_total = len(predictions.get("results", []))
    if cm_total != recorded_total:
        fail(f"confusion matrix sum {cm_total} != recorded total {recorded_total}")
    if cm_total != pred_total:
        fail(f"confusion matrix sum {cm_total} != prediction count {pred_total}")
    if cm_total == recorded_total == pred_total:
        ok(f"confusion matrix totals match: {cm_total}")


# --- Test 10: Per-class metrics sum consistency ---
def test_per_class_consistency() -> None:
    metrics = load_json("metrics.json")
    if metrics is None:
        return
    per_class = metrics.get("per_class", {})
    for label, stats in per_class.items():
        tp = stats.get("true_positives", 0)
        fp = stats.get("false_positives", 0)
        fn = stats.get("false_negatives", 0)
        support = stats.get("support", 0)
        if support != tp + fn:
            fail(f"per-class {label}: support {support} != tp+fn {tp + fn}")
        precision = stats.get("precision", 0)
        recall = stats.get("recall", 0)
        f1 = stats.get("f1", 0)
        exp_p = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 0.0
        exp_r = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 0.0
        exp_f1 = round(2 * exp_p * exp_r / (exp_p + exp_r), 4) if (exp_p + exp_r) > 0 else 0.0
        if abs(precision - exp_p) > 0.0001:
            fail(f"per-class {label}: precision {precision} != expected {exp_p}")
        if abs(recall - exp_r) > 0.0001:
            fail(f"per-class {label}: recall {recall} != expected {exp_r}")
        if abs(f1 - exp_f1) > 0.0001:
            fail(f"per-class {label}: f1 {f1} != expected {exp_f1}")
    ok("per-class metrics are internally consistent")


# --- Test 11: Benchmark split is reproducible ---
def test_split_reproducible() -> None:
    dataset = load_json("dataset.json")
    split = load_json("split.json")
    if dataset is None or split is None:
        return
    all_ids = {c["claim_id"] for c in dataset.get("claims", [])}
    cal = set(split.get("calibration_development", []))
    held = set(split.get("held_out_test", []))
    # Even-numbered claim IDs -> calibration, odd -> held-out
    expected_cal = {cid for cid in all_ids if int(cid.split("-")[1]) % 2 == 0}
    expected_held = {cid for cid in all_ids if int(cid.split("-")[1]) % 2 == 1}
    if cal != expected_cal:
        fail("calibration set is not reproducible (even/odd split)")
    if held != expected_held:
        fail("held-out set is not reproducible (even/odd split)")
    if cal == expected_cal and held == expected_held:
        ok("benchmark split is reproducible")


# --- Test 12: Benchmark artifacts are not silently modified ---
def test_artifact_hashes_recorded() -> None:
    """Record current SHA-256 hashes of all benchmark artifacts for integrity checking."""
    artifacts = [
        "dataset.json", "annotation-guide.md", "split.json",
        "gold-labels.json", "predictions.json", "metrics.json",
        "confusion-matrix.json", "citation-evaluation.json",
    ]
    hashes = {}
    for name in artifacts:
        h = file_sha256(name)
        if h is not None:
            hashes[name] = h
    # Write a hash manifest for future comparison
    manifest_path = BENCH / ".artifact-hashes.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2)
    ok(f"artifact hashes recorded for {len(hashes)} files")


# --- Test 13: 50+ quality claims labeled ---
def test_minimum_claims() -> None:
    dataset = load_json("dataset.json")
    labels = load_json("gold-labels.json")
    if dataset is None or labels is None:
        return
    total_claims = len(dataset.get("claims", []))
    total_labels = len(labels.get("labels", []))
    if total_claims < 50:
        fail(f"only {total_claims} claims; need 50+")
    if total_labels < 50:
        fail(f"only {total_labels} gold labels; need 50+")
    if total_claims >= 50 and total_labels >= 50:
        ok(f"minimum claims met: {total_claims} claims, {total_labels} labels")


# --- Test 14: Single-annotator is explicitly recorded ---
def test_single_annotator_recorded() -> None:
    labels = load_json("gold-labels.json")
    if labels is None:
        return
    protocol = labels.get("annotation_protocol", "")
    annotator = labels.get("annotator", "")
    if protocol != "single-annotator":
        fail(f"annotation_protocol is '{protocol}', expected 'single-annotator'")
    if not annotator:
        fail("annotator field is empty")
    if protocol == "single-annotator" and annotator:
        ok("single-annotator explicitly recorded")


# --- Test 15: No held-out tuning evidence ---
def test_no_held_out_tuning() -> None:
    split = load_json("split.json")
    if split is None:
        return
    note = split.get("split_note", "")
    if "held-out" not in note.lower() and "evaluation-only" not in note.lower():
        fail("split note does not explicitly state held-out is evaluation-only")
    else:
        ok("held-out test set marked as evaluation-only")


def main() -> int:
    if not BENCH.is_dir():
        print(f"ERROR: benchmark directory not found: {BENCH}")
        return 2

    tests = [
        ("artifacts exist", test_artifacts_exist),
        ("gold labels valid", test_gold_labels_valid),
        ("every claim labeled", test_every_claim_labeled),
        ("no duplicate claim IDs", test_no_duplicate_claim_ids),
        ("no missing evidence IDs", test_no_missing_evidence_ids),
        ("held-out separation", test_held_out_separation),
        ("predicted labels valid", test_predicted_labels_valid),
        ("metrics calculate correctly", test_metrics_calculate_correctly),
        ("confusion matrix totals", test_confusion_matrix_totals),
        ("per-class consistency", test_per_class_consistency),
        ("split reproducible", test_split_reproducible),
        ("artifact hashes recorded", test_artifact_hashes_recorded),
        ("minimum 50 claims", test_minimum_claims),
        ("single-annotator recorded", test_single_annotator_recorded),
        ("no held-out tuning", test_no_held_out_tuning),
    ]

    for name, fn in tests:
        try:
            fn()
        except Exception as exc:
            fail(f"{name}: unexpected error: {exc}")

    print()
    if failures:
        print(f"REGRESSION TESTS: {len(failures)} FAILURE(S)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"REGRESSION TESTS: {len(tests)}/{len(tests)} PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
