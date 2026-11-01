============================================================
GOLD-LABELED VERIFICATION BENCHMARK REPORT
============================================================

STATUS:
PARTIAL

------------------------------------------------------------
DATASET
------------------------------------------------------------

Total claims:
72

Human labeled:
72

Calibration:
36

Held-out:
36

Annotators:
1

Agreement:
UNKNOWN (single-annotator; no inter-annotator agreement calculated)

------------------------------------------------------------
HELD-OUT RESULTS
------------------------------------------------------------

Accuracy:
0.3889 (14/36 correct)

Supported:
Precision 1.0000
Recall 0.1765
F1 0.3000

Partially supported:
Precision 0.0000
Recall 0.0000
F1 0.0000

Unsupported:
Precision 0.3000
Recall 0.8571
F1 0.4444

Contradicted:
Precision 0.6250
Recall 0.6250
F1 0.6250

------------------------------------------------------------
CONFUSION MATRIX (gold rows, predicted cols)
------------------------------------------------------------

              SUPPORTED  PARTIAL  UNSUPPORTED  CONTRADICTED
SUPPORTED          3        5          8            1
PARTIAL            0        0          3            1
UNSUPPORTED        0        0          6            1
CONTRADICTED       0        0          3            5

Total: 36

------------------------------------------------------------
SUPPORT DETECTION
------------------------------------------------------------

Supported precision: 1.0000
Supported recall: 0.1765
Supported F1: 0.3000

------------------------------------------------------------
UNSUPPORTED DETECTION
------------------------------------------------------------

Unsupported precision: 0.3000
Unsupported recall: 0.8571
Unsupported F1: 0.4444

------------------------------------------------------------
CONTRADICTION DETECTION
------------------------------------------------------------

Contradiction precision: 0.6250
Contradiction recall: 0.6250
Contradiction F1: 0.6250

------------------------------------------------------------
CITATIONS
------------------------------------------------------------

Citation precision:
UNKNOWN

Citation recall:
UNKNOWN

Citation coverage:
UNKNOWN

Claim-to-source mapping:
UNKNOWN

Reason: Inline citation marker-to-source mapping is unavailable to the verification endpoint. The codebase has no structural representation of answer claim → citation marker → source document → source chunk. Citation IDs exist as string fields in the dataset but are not resolved to actual source documents or chunks by the verification endpoint. The verifier operates on claim text and evidence text directly, with no knowledge of which citation marker in an answer points to which source document.

------------------------------------------------------------
CONFIDENCE
------------------------------------------------------------

Confidence calibration:
LIMITED

High confidence (>=0.80): 10 claims, 7 correct, accuracy 0.7000, avg confidence 0.8769
Medium confidence (0.60-0.79): 6 claims, 1 correct, accuracy 0.1667, avg confidence 0.6833
Low confidence (<0.60): 20 claims, 6 correct, accuracy 0.3000, avg confidence 0.5109

High-confidence predictions are somewhat reliable (70% accuracy) but medium-confidence predictions are poorly calibrated (16.67% accuracy). Overall calibration is LIMITED.

------------------------------------------------------------
HALLUCINATION
------------------------------------------------------------

Unsupported claim rate:
0.1944 (7/36)

Contradicted claim rate:
0.2222 (8/36)

Actual hallucination estimate:
UNKNOWN

Note: UNSUPPORTED and CONTRADICTED are reported separately. The verifier's inverse support percentage is NOT called a hallucination rate. An actual hallucination rate requires knowing which claims require factual support vs. opinion, which is not established in this benchmark.

------------------------------------------------------------
TESTING
------------------------------------------------------------

Benchmark tests:
15/15

Regression:
PASS

Reproducibility:
PASS

Split is deterministic (even claim IDs → calibration, odd → held-out). Artifact hashes recorded for integrity verification.

------------------------------------------------------------
SAFETY
------------------------------------------------------------

Held-out test tuning:
NO

Evaluation manipulated:
NO

Secrets exposed:
NO

Lifecycle changed:
NO

------------------------------------------------------------
BASELINE COMPARISON
------------------------------------------------------------

Historical benchmark (17 calibration cases, not held out):
  Recall: 0.571 (reported previously)

Fresh pre-change:
  Not available (no pre-change benchmark data exists)

Current verifier (held-out gold benchmark):
  Accuracy: 0.3889
  SUPPORTED recall: 0.1765
  UNSUPPORTED recall: 0.8571
  CONTRADICTED recall: 0.6250

These metrics are NOT directly comparable to the historical benchmark because the datasets, label schemes, and evaluation methodology differ. The historical benchmark used only 17 manually labeled cases that were not held out, while this benchmark uses 72 human-labeled claims with a 36/36 calibration/held-out split.

------------------------------------------------------------
DECISION
------------------------------------------------------------

VERIFICATION:
NEEDS MORE WORK

PRIMARY NEXT ACTION:
Implement claim-to-source citation mapping so citation evaluation is possible (cite-D1 → document D1 → specific chunk), then improve the verifier's SUPPORTED recall (currently 0.1765) using only the calibration set. The verifier misclassifies 8 of 17 SUPPORTED held-out claims as UNSUPPORTED — the dominant failure mode. Any algorithm changes must be developed exclusively on the calibration set and validated on a fresh held-out evaluation; the current held-out set must never be used for tuning.

============================================================
