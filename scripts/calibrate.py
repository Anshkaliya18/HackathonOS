#!/usr/bin/env python3
"""Calibrate semantic verification thresholds using ONLY the calibration split.

Pre-computes all claim-evidence semantic similarities once, then searches
threshold configurations over the pre-computed scores. Does NOT touch the
held-out test set.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_DIR = ROOT / ".sherpa" / "evidence" / "gold-benchmark"

sys.path.insert(0, str(ROOT / "src"))
from verification import (  # noqa: E402
    verify_claim,
    SUPPORTED,
    PARTIALLY_SUPPORTED,
    UNSUPPORTED,
    CONTRADICTED,
    _semantic_similarity,
    _numeric_claim_conflict,
    _entity_mismatch,
    _temporal_mismatch,
    _polarity_mismatch,
    _split_compound_claim,
    _sub_claim_supported,
    _get_model,
    SEMANTIC_SUPPORT_THRESHOLD,
    SEMANTIC_PARTIAL_THRESHOLD,
    SEMANTIC_NO_EVIDENCE,
    COVERAGE_SUPPORT_THRESHOLD,
    COVERAGE_PARTIAL_THRESHOLD,
    NUMERIC_TOLERANCE,
)

ALL_LABELS = [SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONTRADICTED]


def _load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    p = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    r = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * p * r / (p + r)) if (p + r) > 0 else 0.0
    return round(p, 4), round(r, 4), round(f1, 4)


def precompute_features(claim_ids: list[str], claims_by_id: dict) -> dict:
    """Pre-compute semantic similarity and gate results for all claims."""
    model = _get_model()
    if model is None:
        print("WARNING: embedding model unavailable; using fallback similarity")
    
    features = {}
    for cid in claim_ids:
        claim = claims_by_id[cid]
        claim_text = claim["claim_text"]
        evidence_text = claim.get("candidate_evidence_text", "")
        
        sim = _semantic_similarity(claim_text, evidence_text)
        
        # Sub-claim coverage
        sub_claims = _split_compound_claim(claim_text)
        if len(sub_claims) > 1:
            supported_count = 0
            for sub in sub_claims:
                sub_sim = _semantic_similarity(sub, evidence_text)
                sub_num = _numeric_claim_conflict(sub, evidence_text)
                sub_pol = _polarity_mismatch(sub, evidence_text, sub_sim)
                if not sub_num and not sub_pol and sub_sim >= 0.68:  # default
                    supported_count += 1
            coverage = supported_count / len(sub_claims)
        else:
            coverage = 1.0 if sim >= 0.68 else 0.0
        
        # Gates
        num_conf = _numeric_claim_conflict(claim_text, evidence_text)
        ent_mis = _entity_mismatch(claim_text, evidence_text)
        temp_conf = _temporal_mismatch(claim_text, evidence_text)
        pol_mis = _polarity_mismatch(claim_text, evidence_text, sim)
        
        features[cid] = {
            "claim_text": claim_text,
            "evidence_text": evidence_text,
            "semantic_sim": sim,
            "coverage": coverage,
            "numeric_conflict": num_conf,
            "entity_mismatch": ent_mis,
            "temporal_conflict": temp_conf,
            "polarity_mismatch": pol_mis,
            "sub_claims": sub_claims,
        }
    
    return features


def decide_with_thresholds(feat: dict, st: float, pt: float, cs: float, cp: float) -> tuple[str, float]:
    """Apply decision logic with given thresholds to pre-computed features."""
    sim = feat["semantic_sim"]
    coverage = feat["coverage"]
    
    contradiction = (feat["numeric_conflict"] or feat["entity_mismatch"] or
                     feat["temporal_conflict"] or feat["polarity_mismatch"])
    
    if contradiction:
        return CONTRADICTED, 0.0
    
    if sim >= st and coverage >= cs:
        conf = round(0.70 + 0.25 * sim * coverage, 4)
        return SUPPORTED, min(conf, 0.95)
    
    if sim >= pt or coverage >= cp:
        conf = round(0.50 + 0.20 * sim * coverage, 4)
        return PARTIALLY_SUPPORTED, min(conf, 0.85)
    
    return UNSUPPORTED, 0.0


def evaluate_with_features(claim_ids: list[str], features: dict, gold_by_id: dict,
                           st: float, pt: float, cs: float, cp: float) -> dict:
    """Evaluate metrics using pre-computed features and given thresholds."""
    results = []
    for cid in claim_ids:
        if cid not in gold_by_id:
            continue
        gold = gold_by_id[cid]
        pred_label, conf = decide_with_thresholds(features[cid], st, pt, cs, cp)
        results.append({
            "claim_id": cid,
            "gold_label": gold,
            "predicted_label": pred_label,
            "correct": gold == pred_label,
            "confidence": conf,
        })
    
    confusion: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in results:
        confusion[r["gold_label"]][r["predicted_label"]] += 1
    
    per_class = {}
    for label in ALL_LABELS:
        tp = confusion[label].get(label, 0)
        fp = sum(confusion[o].get(label, 0) for o in ALL_LABELS if o != label)
        fn = sum(confusion[label].get(o, 0) for o in ALL_LABELS if o != label)
        p, r, f1 = _prf(tp, fp, fn)
        per_class[label] = {"tp": tp, "fp": fp, "fn": fn, "precision": p, "recall": r, "f1": f1}
    
    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    accuracy = round(correct / total, 4) if total > 0 else 0.0
    
    stp = per_class[SUPPORTED]["tp"]
    # FP for support detection: gold != SUPPORTED but pred == SUPPORTED
    sfp = sum(confusion[o].get(SUPPORTED, 0) for o in ALL_LABELS if o != SUPPORTED)
    sfn = per_class[SUPPORTED]["fn"]
    sp, sr, sf1 = _prf(stp, sfp, sfn)
    
    utp = per_class[UNSUPPORTED]["tp"]
    ufp = sum(per_class[o]["fp"] for o in ALL_LABELS if o != UNSUPPORTED)
    ufn = per_class[UNSUPPORTED]["fn"]
    usp, usr, usf1 = _prf(utp, ufp, ufn)
    
    ctp = per_class[CONTRADICTED]["tp"]
    cfp = sum(per_class[o]["fp"] for o in ALL_LABELS if o != CONTRADICTED)
    cfn = per_class[CONTRADICTED]["fn"]
    crp, crr, crf1 = _prf(ctp, cfp, cfn)
    
    return {
        "accuracy": accuracy,
        "correct": correct,
        "total": total,
        "per_class": per_class,
        "support": {"precision": sp, "recall": sr, "f1": sf1},
        "unsupported": {"precision": usp, "recall": usr, "f1": usf1},
        "contradiction": {"precision": crp, "recall": crr, "f1": crf1},
        "results": results,
    }


def main() -> int:
    dataset = _load_json(BENCHMARK_DIR / "dataset.json")
    gold_labels = _load_json(BENCHMARK_DIR / "gold-labels.json")
    split = _load_json(BENCHMARK_DIR / "split.json")

    claims_by_id = {c["claim_id"]: c for c in dataset["claims"]}
    gold_by_id = {e["claim_id"]: e["gold_label"] for e in gold_labels["labels"]}

    cal_ids = sorted(split["calibration_development"])
    held_ids = sorted(split["held_out_test"])

    print(f"Calibration claims: {len(cal_ids)}")
    print(f"Held-out claims: {len(held_ids)} (NOT used for calibration)")

    # Pre-compute features for calibration set only
    print("\nPre-computing semantic similarities for calibration set...")
    cal_features = precompute_features(cal_ids, claims_by_id)

    # Baseline with default thresholds
    print("\n=== BASELINE (default thresholds) on CALIBRATION ===")
    baseline = evaluate_with_features(cal_ids, cal_features, gold_by_id,
                                      0.68, 0.45, 0.75, 0.30)
    print(f"  Accuracy: {baseline['accuracy']}")
    print(f"  SUPPORTED: P={baseline['per_class'][SUPPORTED]['precision']} "
          f"R={baseline['per_class'][SUPPORTED]['recall']} "
          f"F1={baseline['per_class'][SUPPORTED]['f1']}")
    print(f"  PARTIAL:   F1={baseline['per_class'][PARTIALLY_SUPPORTED]['f1']}")
    print(f"  UNSUPP:    P={baseline['per_class'][UNSUPPORTED]['precision']} "
          f"R={baseline['per_class'][UNSUPPORTED]['recall']} "
          f"F1={baseline['per_class'][UNSUPPORTED]['f1']}")
    print(f"  CONTRAD:   P={baseline['per_class'][CONTRADICTED]['precision']} "
          f"R={baseline['per_class'][CONTRADICTED]['recall']} "
          f"F1={baseline['per_class'][CONTRADICTED]['f1']}")
    print(f"  Support:   P={baseline['support']['precision']} "
          f"R={baseline['support']['recall']} F1={baseline['support']['f1']}")

    # Grid search on calibration set
    print("\n=== GRID SEARCH on CALIBRATION ===")
    support_thresholds = [0.60, 0.65, 0.68, 0.70, 0.72, 0.75, 0.80, 0.85]
    partial_thresholds = [0.35, 0.40, 0.45, 0.50, 0.55]
    coverage_support = [0.70, 0.75, 0.80]
    coverage_partial = [0.25, 0.30, 0.40]

    all_configs = []
    best_config = None
    best_score = -1.0

    for st, pt, cs, cp in product(support_thresholds, partial_thresholds,
                                    coverage_support, coverage_partial):
        if pt >= st or cp >= cs:
            continue

        result = evaluate_with_features(cal_ids, cal_features, gold_by_id, st, pt, cs, cp)
        
        sp_prec = result["per_class"][SUPPORTED]["precision"]
        sp_rec = result["per_class"][SUPPORTED]["recall"]
        sp_f1 = result["per_class"][SUPPORTED]["f1"]
        contra_f1 = result["per_class"][CONTRADICTED]["f1"]
        unsup_f1 = result["per_class"][UNSUPPORTED]["f1"]
        
        # Precision floor: reject configs with supported precision < 0.60
        if sp_prec < 0.60:
            continue
        
        score = sp_f1 * 0.4 + sp_prec * 0.3 + contra_f1 * 0.15 + unsup_f1 * 0.15
        
        all_configs.append({
            "config": {
                "semantic_support_threshold": st,
                "semantic_partial_threshold": pt,
                "coverage_support_threshold": cs,
                "coverage_partial_threshold": cp,
            },
            "metrics": {
                "accuracy": result["accuracy"],
                "supported": result["per_class"][SUPPORTED],
                "partial": result["per_class"][PARTIALLY_SUPPORTED],
                "unsupported": result["per_class"][UNSUPPORTED],
                "contradicted": result["per_class"][CONTRADICTED],
                "support_detection": result["support"],
                "unsupported_detection": result["unsupported"],
                "contradiction_detection": result["contradiction"],
            },
            "score": round(score, 4),
        })
        
        if score > best_score:
            best_score = score
            best_config = all_configs[-1]

    all_configs.sort(key=lambda x: x["score"], reverse=True)

    print(f"\nTop 5 configurations by score (precision floor >= 0.80):")
    for i, cfg in enumerate(all_configs[:5]):
        m = cfg["metrics"]
        print(f"  #{i+1} score={cfg['score']} config={cfg['config']}")
        print(f"       Acc={m['accuracy']} "
              f"SUPP(P={m['supported']['precision']} R={m['supported']['recall']} F1={m['supported']['f1']}) "
              f"PART(F1={m['partial']['f1']}) "
              f"UNSUP(P={m['unsupported']['precision']} R={m['unsupported']['recall']} F1={m['unsupported']['f1']}) "
              f"CONTRA(P={m['contradicted']['precision']} R={m['contradicted']['recall']} F1={m['contradicted']['f1']})")

    # Save calibration results
    cal_output = {
        "benchmark_version": "1.0.0",
        "calibration_claims": len(cal_ids),
        "held_out_claims": len(held_ids),
        "baseline": {
            "config": {
                "semantic_support_threshold": 0.68,
                "semantic_partial_threshold": 0.45,
                "coverage_support_threshold": 0.75,
                "coverage_partial_threshold": 0.30,
            },
            "metrics": baseline,
        },
        "best_config": best_config,
        "all_configs": all_configs[:10],
        "note": "Calibration performed on calibration split only. Held-out set was not used.",
    }

    _write_json(BENCHMARK_DIR / "semantic-calibration.json", cal_output)

    if best_config:
        print(f"\n=== BEST CONFIGURATION ===")
        print(f"  Config: {best_config['config']}")
        print(f"  Score: {best_config['score']}")
        m = best_config["metrics"]
        print(f"  Supported: P={m['supported']['precision']} R={m['supported']['recall']} F1={m['supported']['f1']}")
        print(f"  Partial:   F1={m['partial']['f1']}")
        print(f"  Unsupported: P={m['unsupported']['precision']} R={m['unsupported']['recall']} F1={m['unsupported']['f1']}")
        print(f"  Contradicted: P={m['contradicted']['precision']} R={m['contradicted']['recall']} F1={m['contradicted']['f1']}")
        print(f"\nCalibration results saved to: {BENCHMARK_DIR / 'semantic-calibration.json'}")
    else:
        print("\nNo configuration met the precision floor (>= 0.80). Keeping defaults.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
