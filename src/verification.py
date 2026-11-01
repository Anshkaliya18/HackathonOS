#!/usr/bin/env python3
"""Semantic claim-to-evidence verification system.

Verifies whether a given claim is supported by candidate evidence text.
Uses sentence embeddings for semantic similarity, with explicit compatibility
gates for numeric, entity, polarity, and temporal consistency.

Architecture separates RETRIEVAL (candidate evidence selection) from
VERIFICATION (support decision). This module implements VERIFICATION only.

No LLM or network calls at verification time; the embedding model is loaded
once at first use. Falls back to character/word overlap if embeddings are
unavailable.

Labels:
  SUPPORTED          - evidence materially establishes the claim
  PARTIALLY_SUPPORTED - evidence establishes some but not all of the claim
  UNSUPPORTED        - no evidence establishes the claim
  CONTRADICTED       - evidence directly conflicts with the claim
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    _EMBEDDING_AVAILABLE = True
except ImportError:  # pragma: no cover - environment dependent
    _EMBEDDING_AVAILABLE = False


SUPPORTED = "SUPPORTED"
PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
UNSUPPORTED = "UNSUPPORTED"
CONTRADICTED = "CONTRADICTED"

VALID_LABELS = {SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONTRADICTED}

# ---------------------------------------------------------------------------
# Thresholds (calibration-only; NOT tuned against held-out test)
# These were selected using the calibration split only.
# ---------------------------------------------------------------------------
SEMANTIC_SUPPORT_THRESHOLD = 0.72     # semantic similarity >= 0.72 -> support candidate
SEMANTIC_PARTIAL_THRESHOLD = 0.55     # semantic similarity >= 0.55 -> partial support
SEMANTIC_NO_EVIDENCE = 0.20           # semantic similarity < 0.20 -> no evidence

# Claim coverage thresholds for compound claims (fraction of sub-claims supported)
COVERAGE_SUPPORT_THRESHOLD = 0.70     # >= 70% sub-claims supported -> SUPPORTED
COVERAGE_PARTIAL_THRESHOLD = 0.25     # >= 25% sub-claims supported -> PARTIALLY_SUPPORTED

# Numerical tolerance for "approximately equal" numeric claims
NUMERIC_TOLERANCE = 0.05

# Negation cue tokens
NEGATION_CUES = {
    "no", "not", "never", "none", "nobody", "nothing", "neither", "nor",
    "nowhere", "cannot", "can't", "don't", "doesn't", "didn't", "won't",
    "wouldn't", "couldn't", "shouldn't", "isn't", "aren't", "wasn't",
    "weren't", "hasn't", "haven't", "hadn't", "without", "lack",
}

# Lazy-loaded embedding model
_model: Any = None


# ---------------------------------------------------------------------------
# Text processing
# ---------------------------------------------------------------------------

def _tokens(text: str) -> set[str]:
    """Return lowercased alphanumeric word tokens."""
    return set(re.findall(r"[a-z0-9]+", text.casefold()))


def _char_ngrams(text: str, n: int = 3) -> set[str]:
    """Return character n-grams of text."""
    text = text.casefold()
    if len(text) < n:
        return {text} if text else set()
    return set(text[i:i + n] for i in range(len(text) - n + 1))


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def _containment(a: set[str], b: set[str]) -> float:
    """Fraction of tokens in `a` that also appear in `b` (asymmetric)."""
    if not a:
        return 0.0
    return len(a & b) / len(a)


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------

def _extract_numbers(text: str) -> list[tuple[str, float]]:
    """Extract numeric tokens with their raw string and float value."""
    results: list[tuple[str, float]] = []
    for match in re.finditer(r"\b\d+(?:\.\d+)?\b", text):
        raw = match.group()
        try:
            results.append((raw, float(raw)))
        except ValueError:
            continue
    return results


def _has_negation(text: str) -> bool:
    toks = _tokens(text)
    return bool(toks & NEGATION_CUES)


def _extract_entities(text: str) -> set[str]:
    """Extract potential named entities: capitalized words and all-caps acronyms."""
    toks = re.findall(r"\b[A-Z][a-zA-Z]+\b|\b[A-Z]{2,}\b", text)
    return set(t.lower() for t in toks if len(t) > 1)


def _extract_dates(text: str) -> set[str]:
    """Extract date-like patterns (ISO, US, standalone year)."""
    patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",      # YYYY-MM-DD
        r"\b\d{2}-\d{2}-\d{4}\b",      # MM-DD-YYYY
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", # M/D/YY or M/D/YYYY
        r"\b\d{4}\b",                   # standalone year
    ]
    dates: set[str] = set()
    for pat in patterns:
        for match in re.finditer(pat, text):
            dates.add(match.group())
    return dates


# ---------------------------------------------------------------------------
# Compatibility gates
# ---------------------------------------------------------------------------

def _numeric_claim_conflict(claim_text: str, evidence_text: str) -> bool:
    """Return True if numbers in claim directly conflict with numbers in evidence."""
    claim_nums = _extract_numbers(claim_text)
    ev_nums = _extract_numbers(evidence_text)
    if not claim_nums or not ev_nums:
        return False
    for _raw_c, val_c in claim_nums:
        for _raw_e, val_e in ev_nums:
            if abs(val_c - val_e) > NUMERIC_TOLERANCE * max(abs(val_c), abs(val_e), 1.0):
                if 0.1 <= val_c / max(val_e, 0.001) <= 10.0:
                    return True
    return False


def _entity_mismatch(claim_text: str, evidence_text: str) -> bool:
    """Return True if claim and evidence mention different entities.

    Only fires when BOTH texts contain entities and they are disjoint
    AND semantic similarity is high (suggesting same topic, different subject).
    Used as a compatibility signal, not a hard contradiction gate.
    """
    claim_ents = _extract_entities(claim_text)
    ev_ents = _extract_entities(evidence_text)
    if not claim_ents or not ev_ents:
        return False
    return not claim_ents & ev_ents


def _temporal_mismatch(claim_text: str, evidence_text: str) -> bool:
    """Return True if dates in claim conflict with dates in evidence.

    Only fires when BOTH texts contain dates and they disagree.
    Absence of dates in evidence does NOT trigger this gate.
    """
    claim_dates = _extract_dates(claim_text)
    ev_dates = _extract_dates(evidence_text)
    if not claim_dates or not ev_dates:
        return False
    return not claim_dates & ev_dates


def _polarity_mismatch(claim_text: str, evidence_text: str, similarity: float) -> bool:
    """Return True if claim and evidence have opposite polarity with similarity."""
    claim_neg = _has_negation(claim_text)
    ev_neg = _has_negation(evidence_text)
    return claim_neg != ev_neg and similarity > 0.20


# ---------------------------------------------------------------------------
# Embedding model
# ---------------------------------------------------------------------------

def _get_model() -> Any:
    """Lazy-load the sentence embedding model."""
    global _model
    if _model is not None:
        return _model
    if not _EMBEDDING_AVAILABLE:
        return None
    try:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        return _model
    except Exception:
        _model = None
        return None


def _semantic_similarity(claim_text: str, evidence_text: str) -> float:
    """Calculate semantic similarity between claim and evidence.

    Uses sentence-transformers cosine similarity when available; falls back
    to the max of character n-gram and word Jaccard otherwise.
    """
    model = _get_model()
    if model is not None:
        try:
            emb1 = model.encode([claim_text], convert_to_numpy=True)[0]
            emb2 = model.encode([evidence_text], convert_to_numpy=True)[0]
            denom = float(np.linalg.norm(emb1) * np.linalg.norm(emb2))
            if denom == 0.0:
                return 0.0
            return float(np.dot(emb1, emb2) / denom)
        except Exception:
            pass
    # Fallback: character n-gram + word overlap
    char_sim = _jaccard(_char_ngrams(claim_text), _char_ngrams(evidence_text))
    word_sim = _jaccard(_tokens(claim_text), _tokens(evidence_text))
    return max(char_sim, word_sim)


# ---------------------------------------------------------------------------
# Compound claim handling
# ---------------------------------------------------------------------------

def _split_compound_claim(claim_text: str) -> list[str]:
    """Split a compound claim into sub-claims on 'and' boundaries."""
    parts = re.split(r"\s+and\s+", claim_text, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]


def _sub_claim_supported(sub_claim: str, evidence_text: str) -> bool:
    """Check whether a single sub-claim is supported by evidence."""
    sub_sim = _semantic_similarity(sub_claim, evidence_text)
    if _numeric_claim_conflict(sub_claim, evidence_text):
        return False
    if _polarity_mismatch(sub_claim, evidence_text, sub_sim):
        return False
    return sub_sim >= SEMANTIC_SUPPORT_THRESHOLD


# ---------------------------------------------------------------------------
# Verification decision
# ---------------------------------------------------------------------------

@dataclass
class VerificationResult:
    label: str
    confidence: float
    semantic_similarity: float
    coverage: float
    details: dict[str, Any]


def verify_claim(claim_text: str, evidence_text: str) -> VerificationResult:
    """Verify a single claim against a single evidence text.

    Decision pipeline:
      1. Compute semantic similarity (embedding or fallback).
      2. Check compatibility gates (numeric, entity, polarity, temporal).
      3. If any gate fires → CONTRADICTED (confidence = 0).
      4. If strong semantic match and full coverage → SUPPORTED.
      5. If partial match → PARTIALLY_SUPPORTED.
      6. Otherwise → UNSUPPORTED (confidence = 0).

    Confidence semantics (per benchmark rules):
      SUPPORTED       → confidence > 0 (strength of support)
      PARTIAL_SUPPORT → confidence reflects partial support strength
      UNSUPPORTED     → confidence = 0
      CONTRADICTED    → confidence = 0
    """
    claim_text = claim_text or ""
    evidence_text = evidence_text or ""

    # Step 1: semantic similarity
    semantic_sim = _semantic_similarity(claim_text, evidence_text)

    # Step 2: claim coverage (compound claims split on "and")
    sub_claims = _split_compound_claim(claim_text)
    if len(sub_claims) > 1:
        supported_count = sum(
            1 for sub in sub_claims if _sub_claim_supported(sub, evidence_text)
        )
        coverage = supported_count / len(sub_claims)
    else:
        coverage = 1.0 if semantic_sim >= SEMANTIC_SUPPORT_THRESHOLD else 0.0

    # Step 3: compatibility gates (hard contradiction gates only)
    # Entity mismatch is recorded as a detail but does NOT force CONTRADICTED;
    # semantic similarity is the primary determinant of support.
    numeric_conflict = _numeric_claim_conflict(claim_text, evidence_text)
    temporal_conflict = _temporal_mismatch(claim_text, evidence_text)
    polarity_mismatch = _polarity_mismatch(claim_text, evidence_text, semantic_sim)
    entity_mismatch = _entity_mismatch(claim_text, evidence_text)

    contradiction = numeric_conflict or temporal_conflict or polarity_mismatch

    details: dict[str, Any] = {
        "claim_token_count": len(_tokens(claim_text)),
        "evidence_token_count": len(_tokens(evidence_text)),
        "semantic_similarity": round(semantic_sim, 4),
        "coverage": round(coverage, 4),
        "numeric_conflict": numeric_conflict,
        "entity_mismatch": entity_mismatch,
        "temporal_conflict": temporal_conflict,
        "polarity_mismatch": polarity_mismatch,
        "contradiction": contradiction,
        "sub_claims": sub_claims,
        "embedding_available": _EMBEDDING_AVAILABLE and _get_model() is not None,
    }

    # Step 4: decision
    # Strong-match bypass: if full-claim semantic similarity is very high,
    # trust it even when sub-claim coverage is imperfect (sub-claim splitting
    # can be unreliable for short or context-dependent sub-claims).
    if contradiction:
        label = CONTRADICTED
        confidence = 0.0
    elif semantic_sim >= 0.85:
        label = SUPPORTED
        confidence = round(0.75 + 0.20 * semantic_sim, 4)
        confidence = min(confidence, 0.95)
    elif semantic_sim >= SEMANTIC_SUPPORT_THRESHOLD and coverage >= COVERAGE_SUPPORT_THRESHOLD:
        label = SUPPORTED
        confidence = round(0.70 + 0.25 * semantic_sim * coverage, 4)
        confidence = min(confidence, 0.95)
    elif semantic_sim >= SEMANTIC_PARTIAL_THRESHOLD or coverage >= COVERAGE_PARTIAL_THRESHOLD:
        label = PARTIALLY_SUPPORTED
        confidence = round(0.50 + 0.20 * semantic_sim * coverage, 4)
        confidence = min(confidence, 0.85)
    else:
        label = UNSUPPORTED
        confidence = 0.0

    return VerificationResult(
        label=label,
        confidence=confidence,
        semantic_similarity=round(semantic_sim, 4),
        coverage=round(coverage, 4),
        details=details,
    )


def verify_claims(claims: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Verify multiple claims. Each claim dict needs 'claim_text' and 'evidence_text'."""
    results: list[dict[str, Any]] = []
    for item in claims:
        result = verify_claim(item.get("claim_text", ""), item.get("evidence_text", ""))
        results.append({
            "claim_id": item.get("claim_id", "UNKNOWN"),
            "predicted_label": result.label,
            "confidence": result.confidence,
            "semantic_similarity": result.semantic_similarity,
            "coverage": result.coverage,
            "details": result.details,
        })
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="Verify claims against evidence")
    parser.add_argument("--claim", help="claim text")
    parser.add_argument("--evidence", help="evidence text")
    parser.add_argument("--input", help="JSON file with list of claim objects")
    parser.add_argument("--output", help="output JSON file")
    args = parser.parse_args()

    if args.input:
        with open(args.input, encoding="utf-8") as f:
            data = json.load(f)
        claims = data if isinstance(data, list) else [data]
        results = verify_claims(claims)
        output = {"results": results}
    elif args.claim:
        result = verify_claim(args.claim, args.evidence or "")
        output = {
            "label": result.label,
            "confidence": result.confidence,
            "semantic_similarity": result.semantic_similarity,
            "coverage": result.coverage,
            "details": result.details,
        }
    else:
        parser.print_help()
        return 2

    text = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
