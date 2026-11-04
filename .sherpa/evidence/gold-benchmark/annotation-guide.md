# sherpa Gold-Labeled Verification Benchmark — Annotation Guide

## Purpose

This document defines the human annotation protocol for the gold-labeled verification benchmark. Human labels are the ground truth. The verifier is evaluated against these labels without being tuned to them.

## Label Definitions

Each claim is labeled with exactly one of the following:

| Label | Definition |
|-------|------------|
| **SUPPORTED** | The cited evidence materially establishes the claim. All key elements of the claim are directly confirmed by the evidence. |
| **PARTIALLY_SUPPORTED** | The evidence establishes some but not all elements of the claim. At least one key element is confirmed, but at least one is missing or unconfirmed. |
| **UNSUPPORTED** | No evidence in the cited source establishes the claim. The claim may be true or false, but the cited evidence does not support it. This includes claims where the cited evidence is irrelevant or silent on the claim. |
| **CONTRADICTED** | The cited evidence directly conflicts with the claim. The evidence states something incompatible with the claim (different number, opposite negation, different entity, etc.). |

### Distinguishing UNSUPPORTED from CONTRADICTED

- **UNSUPPORTED**: The evidence says nothing about the claim, or is about a different topic. Absence of support.
- **CONTRADICTED**: The evidence says something that directly opposes the claim. Presence of conflicting information.

Example:
- Claim: "The system has twelve components." Evidence: "The system has eleven components." → CONTRADICTED
- Claim: "The system has twelve components." Evidence: (no mention of component count) → UNSUPPORTED

## Annotation Task

For each claim, answer:

> "Does this evidence actually support this specific claim?"

Not:

> "Does this document look related?"

A citation is valid only when the evidence materially supports the claim.

## Annotation Artifact Fields

| Field | Description |
|-------|-------------|
| claim_id | Unique identifier for the claim |
| question_id | ID of the question the claim belongs to |
| claim_text | The claim text being evaluated |
| candidate_evidence_id | ID of the evidence cited for this claim |
| evidence_text | The text of the cited evidence |
| gold_label | One of: SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONTRADICTED |
| annotator | Identifier of the human annotator |
| annotation_reason | Brief explanation of why this label was assigned |

## Annotator Information

- **Annotator**: single-annotator (human-1)
- **Inter-annotator agreement**: NOT APPLICABLE — only one annotator is available. No Cohen's kappa or agreement rate is calculated. This limitation is explicitly recorded.

## Examples

### SUPPORTED

Claim: "The system has twelve components."
Evidence: "The system explicitly has twelve components."
Label: SUPPORTED
Reason: Evidence explicitly states twelve components, matching the claim exactly.

### CONTRADICTED (numerical conflict)

Claim: "The system has twelve components."
Evidence: "The system has eleven components."
Label: CONTRADICTED
Reason: Evidence states a different number (eleven vs twelve) for the same quantity.

### PARTIALLY_SUPPORTED

Claim: "The system uses Python and provides real-time monitoring."
Evidence: "The system uses Python."
Label: PARTIALLY_SUPPORTED
Reason: Evidence establishes Python but says nothing about real-time monitoring.

### UNSUPPORTED

Claim: "The system reduced costs by 40%."
Evidence: (no mention of cost reduction)
Label: UNSUPPORTED
Reason: No evidence establishes the 40% cost reduction claim.

### Citation mismatch

Claim: "sherpa has a UX review workflow."
Evidence: "Deterministic command argument routing. Validates manifest schema_version=1."
Label: UNSUPPORTED
Reason: The cited evidence (command routing) does not mention UX review. The claim may be true elsewhere, but this citation does not support it.

## Label Distribution Target

The benchmark includes claims across these categories:
1. Direct factual claims
2. Numerical claims
3. Dates
4. Named entities
5. Negation
6. Compound claims
7. Partial evidence
8. Contradictory evidence
9. Irrelevant but semantically similar evidence
10. Unsupported claims
11. Multi-sentence answers
12. Citation mismatch
13. Claims supported by different documents
14. Claims with no valid evidence

## Rules for Annotators

1. Label based only on the cited evidence, not on external knowledge.
2. Do not infer support from semantic similarity alone.
3. A claim citing the wrong source is UNSUPPORTED (citation mismatch), even if the claim is true.
4. Numerical mismatches are CONTRADICTED, not UNSUPPORTED.
5. Negation mismatches are CONTRADICTED when the rest of the claim matches.
6. Compound claims where one part is supported and one is not are PARTIALLY_SUPPORTED.
7. Do not label automatically. Do not use the verifier to create gold labels.
8. Record single-annotator status explicitly. Do not fabricate inter-annotator agreement.
