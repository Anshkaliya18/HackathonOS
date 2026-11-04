#!/usr/bin/env python3
"""Evaluate the verification system against the gold-labeled benchmark.

Loads dataset.json, gold-labels.json, and split.json from
.sherpa/evidence/gold-benchmark/, runs the verifier on held-out test claims,
and writes predictions.json, metrics.json, confusion-matrix.json,
citation-evaluation.json to the same directory.

Does NOT tune thresholds against the held-out test set.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_DIR = ROOT / ".sherpa" / "evidence" / "gold-benchmark"

# Import the verifier from src/
sys.path.insert(0, str(ROOT / "src"))
from verification import verify_claims, SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONTRADICTED  # noqa: E402

ALL_LABELS = [SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONTRADICTED]


def _load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _precision_recall_f1(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    return round(precision, 4), round(recall, 4), round(f1, 4)


def evaluate() -> dict[str, Any]:
    dataset = _load_json(BENCHMARK_DIR / "dataset.json")
    gold_labels = _load_json(BENCHMARK_DIR / "gold-labels.json")
    split = _load_json(BENCHMARK_DIR / "split.json")

    held_out_ids = set(split["held_out_test"])
    calibration_ids = set(split["calibration_development"])

    # Build lookup from claim_id -> claim record
    claims_by_id: dict[str, dict[str, Any]] = {}
    for claim in dataset["claims"]:
        claims_by_id[claim["claim_id"]] = claim

    # Build lookup from claim_id -> gold label
    gold_by_id: dict[str, str] = {}
    for entry in gold_labels["labels"]:
        gold_by_id[entry["claim_id"]] = entry["gold_label"]

    # Verify held-out claims only
    held_out_claims = []
    for cid in sorted(held_out_ids):
        if cid not in claims_by_id:
            continue
        claim = claims_by_id[cid]
        held_out_claims.append({
            "claim_id": cid,
            "claim_text": claim["claim_text"],
            "evidence_text": claim.get("candidate_evidence_text", ""),
        })

    predictions = verify_claims(held_out_claims)

    # Build prediction lookup
    pred_by_id: dict[str, dict[str, Any]] = {}
    for p in predictions:
        pred_by_id[p["claim_id"]] = p

    # --- Per-claim result records ---
    claim_results = []
    for cid in sorted(held_out_ids):
        if cid not in claims_by_id or cid not in gold_by_id or cid not in pred_by_id:
            continue
        claim = claims_by_id[cid]
        gold = gold_by_id[cid]
        pred = pred_by_id[cid]
        claim_results.append({
            "claim_id": cid,
            "question_id": claim.get("question_id", "UNKNOWN"),
            "claim_text": claim["claim_text"],
            "category": claim.get("category", "UNKNOWN"),
            "gold_label": gold,
            "predicted_label": pred["predicted_label"],
            "correct": gold == pred["predicted_label"],
            "confidence": pred["confidence"],
            "semantic_similarity": pred.get("semantic_similarity", 0.0),
            "coverage": pred.get("coverage", 0.0),
            "evidence_id": claim.get("candidate_evidence_id", "UNKNOWN"),
            "citation_id": claim.get("citation_id", "UNKNOWN"),
        })

    _write_json(BENCHMARK_DIR / "predictions.json", {
        "benchmark_version": "1.0.0",
        "total_held_out": len(claim_results),
        "calibration_count": len(calibration_ids),
        "held_out_count": len(held_out_ids),
        "results": claim_results,
    })

    # --- Overall metrics ---
    total = len(claim_results)
    correct = sum(1 for r in claim_results if r["correct"])
    accuracy = round(correct / total, 4) if total > 0 else 0.0

    # --- Per-class metrics ---
    per_class = {}
    confusion: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for r in claim_results:
        confusion[r["gold_label"]][r["predicted_label"]] += 1

    for label in ALL_LABELS:
        tp = confusion[label].get(label, 0)
        fp = sum(confusion[other].get(label, 0) for other in ALL_LABELS if other != label)
        fn = sum(confusion[label].get(other, 0) for other in ALL_LABELS if other != label)
        p, r, f1 = _precision_recall_f1(tp, fp, fn)
        per_class[label] = {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "precision": p,
            "recall": r,
            "f1": f1,
            "support": tp + fn,
        }

    # --- Confusion matrix (gold rows, predicted cols) ---
    confusion_matrix = {
        "labels": ALL_LABELS,
        "matrix": {label: {other: confusion[label].get(other, 0) for other in ALL_LABELS} for label in ALL_LABELS},
        "total": total,
    }

    _write_json(BENCHMARK_DIR / "confusion-matrix.json", confusion_matrix)

    # --- Support detection (SUPPORTED vs not-SUPPORTED) ---
    support_tp = sum(1 for r in claim_results if r["gold_label"] == SUPPORTED and r["predicted_label"] == SUPPORTED)
    support_fp = sum(1 for r in claim_results if r["gold_label"] != SUPPORTED and r["predicted_label"] == SUPPORTED)
    support_fn = sum(1 for r in claim_results if r["gold_label"] == SUPPORTED and r["predicted_label"] != SUPPORTED)
    sp, sr, sf1 = _precision_recall_f1(support_tp, support_fp, support_fn)

    # --- Unsupported detection (UNSUPPORTED vs not-UNSUPPORTED) ---
    unsup_tp = sum(1 for r in claim_results if r["gold_label"] == UNSUPPORTED and r["predicted_label"] == UNSUPPORTED)
    unsup_fp = sum(1 for r in claim_results if r["gold_label"] != UNSUPPORTED and r["predicted_label"] == UNSUPPORTED)
    unsup_fn = sum(1 for r in claim_results if r["gold_label"] == UNSUPPORTED and r["predicted_label"] != UNSUPPORTED)
    usp, usr, usf1 = _precision_recall_f1(unsup_tp, unsup_fp, unsup_fn)

    # --- Contradiction detection (CONTRADICTED vs not-CONTRADICTED) ---
    contra_tp = sum(1 for r in claim_results if r["gold_label"] == CONTRADICTED and r["predicted_label"] == CONTRADICTED)
    contra_fp = sum(1 for r in claim_results if r["gold_label"] != CONTRADICTED and r["predicted_label"] == CONTRADICTED)
    contra_fn = sum(1 for r in claim_results if r["gold_label"] == CONTRADICTED and r["predicted_label"] != CONTRADICTED)
    crp, crr, crf1 = _precision_recall_f1(contra_tp, contra_fp, contra_fn)

    # --- Confidence calibration ---
    # Bin predictions by confidence and check correctness within each bin
    conf_bins: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in claim_results:
        conf = r["confidence"]
        if conf >= 0.80:
            bin_key = "high (>=0.80)"
        elif conf >= 0.60:
            bin_key = "medium (0.60-0.79)"
        else:
            bin_key = "low (<0.60)"
        conf_bins[bin_key].append(r)

    calibration = {}
    for bin_key, bins_results in sorted(conf_bins.items()):
        bin_correct = sum(1 for r in bins_results if r["correct"])
        bin_total = len(bins_results)
        calibration[bin_key] = {
            "count": bin_total,
            "correct": bin_correct,
            "accuracy": round(bin_correct / bin_total, 4) if bin_total > 0 else 0.0,
            "avg_confidence": round(sum(r["confidence"] for r in bins_results) / bin_total, 4) if bin_total > 0 else 0.0,
        }

    # Overall calibration assessment
    high_conf = calibration.get("high (>=0.80)", {})
    high_conf_accuracy = high_conf.get("accuracy", 0.0)
    high_conf_count = high_conf.get("count", 0)
    if high_conf_count >= 5:
        calibration_assessment = "GOOD" if high_conf_accuracy >= 0.75 else "LIMITED"
    elif high_conf_count > 0:
        calibration_assessment = "LIMITED"
    else:
        calibration_assessment = "UNKNOWN"

    # --- Citation evaluation ---
    # A citation is correct only when the cited evidence actually supports the claim.
    # Since the architecture lacks claim-to-source mapping (inline citation marker
    # to source document/chunk), exact claim-to-source evaluation is impossible.
    citation_evaluation = {
        "claim_to_source_mapping": "UNKNOWN",
        "reason": "Inline citation marker-to-source mapping is unavailable to the verification endpoint. Citation IDs exist in the dataset but no structural mapping from answer claim → citation marker → source document → source chunk is represented in the codebase.",
        "citation_precision": "UNKNOWN",
        "citation_recall": "UNKNOWN",
        "citation_coverage": "UNKNOWN",
    }

    # --- Hallucination metric ---
    # Define: hallucinated/unsupported claims = claims where gold is UNSUPPORTED or CONTRADICTED
    # (claims requiring factual support that are not actually supported)
    factual_support_claims = [r for r in claim_results if r["gold_label"] in (SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONTRADICTED)]
    unsupported_count = sum(1 for r in claim_results if r["gold_label"] == UNSUPPORTED)
    contradicted_count = sum(1 for r in claim_results if r["gold_label"] == CONTRADICTED)
    unsupported_rate = round(unsupported_count / total, 4) if total > 0 else 0.0
    contradicted_rate = round(contradicted_count / total, 4) if total > 0 else 0.0

    # "Actual hallucination estimate" - we cannot call the verifier's inverse support
    # percentage a hallucination rate. We report the human-gold-based rates.
    hallucination_estimate = "UNKNOWN"  # Cannot estimate without knowing which claims require factual support vs opinion

    metrics = {
        "benchmark_version": "1.0.0",
        "dataset_info": {
            "total_claims": len(dataset["claims"]),
            "calibration_count": len(calibration_ids),
            "held_out_count": len(held_out_ids),
            "evaluated_count": total,
            "annotators": "single-annotator",
        },
        "overall": {
            "accuracy": accuracy,
            "correct": correct,
            "total": total,
        },
        "per_class": per_class,
        "support_detection": {
            "true_positives": support_tp,
            "false_positives": support_fp,
            "false_negatives": support_fn,
            "precision": sp,
            "recall": sr,
            "f1": sf1,
        },
        "unsupported_detection": {
            "true_positives": unsup_tp,
            "false_positives": unsup_fp,
            "false_negatives": unsup_fn,
            "precision": usp,
            "recall": usr,
            "f1": usf1,
        },
        "contradiction_detection": {
            "true_positives": contra_tp,
            "false_positives": contra_fp,
            "false_negatives": contra_fn,
            "precision": crp,
            "recall": crr,
            "f1": crf1,
        },
        "confidence_calibration": calibration,
        "calibration_assessment": calibration_assessment,
        "citation_evaluation": citation_evaluation,
        "hallucination": {
            "unsupported_claim_rate": unsupported_rate,
            "contradicted_claim_rate": contradicted_rate,
            "unsupported_count": unsupported_count,
            "contradicted_count": contradicted_count,
            "actual_hallucination_estimate": hallucination_estimate,
            "note": "UNSUPPORTED and CONTRADICTED are reported separately. The verifier's inverse support percentage is NOT called a hallucination rate.",
        },
    }

    _write_json(BENCHMARK_DIR / "metrics.json", metrics)

    return metrics


def main() -> int:
    if not BENCHMARK_DIR.is_dir():
        print(f"ERROR: benchmark directory not found: {BENCHMARK_DIR}")
        return 2
    for required in ("dataset.json", "gold-labels.json", "split.json"):
        if not (BENCHMARK_DIR / required).is_file():
            print(f"ERROR: missing required artifact: {required}")
            return 2

    metrics = evaluate()

    print(f"Evaluation complete.")
    print(f"  Held-out claims evaluated: {metrics['overall']['total']}")
    print(f"  Accuracy: {metrics['overall']['accuracy']}")
    print(f"  Calibration assessment: {metrics['calibration_assessment']}")
    print(f"  Citation mapping: {metrics['citation_evaluation']['claim_to_source_mapping']}")
    print(f"  Unsupported claim rate: {metrics['hallucination']['unsupported_claim_rate']}")
    print(f"  Contradicted claim rate: {metrics['hallucination']['contradicted_claim_rate']}")
    print(f"  Outputs written to: {BENCHMARK_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
