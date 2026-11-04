import json, sys
sys.path.insert(0, 'src')
from verification import (_semantic_similarity, _numeric_claim_conflict, _entity_mismatch,
                          _temporal_mismatch, _polarity_mismatch, _split_compound_claim, _get_model)

with open('.sherpa/evidence/gold-benchmark/gold-labels.json') as f:
    labels = json.load(f)['labels']
with open('.sherpa/evidence/gold-benchmark/split.json') as f:
    split = json.load(f)

cal_ids = set(split['calibration_development'])
model = _get_model()
print(f'Model loaded: {model is not None}')
print()

for entry in labels:
    cid = entry['claim_id']
    if cid not in cal_ids:
        continue
    gold = entry['gold_label']
    claim = entry['claim_text']
    ev = entry['evidence_text']

    sim = _semantic_similarity(claim, ev)
    num = _numeric_claim_conflict(claim, ev)
    ent = _entity_mismatch(claim, ev)
    temp = _temporal_mismatch(claim, ev)
    pol = _polarity_mismatch(claim, ev, sim)
    contra = num or ent or temp or pol

    sub_claims = _split_compound_claim(claim)

    flag = ' <<< SUPPORTED' if gold == 'SUPPORTED' else ''
    print(f'{cid} gold={gold:18s} sim={sim:.3f} num={num} ent={ent} temp={temp} pol={pol} contra={contra}{flag}')
    if gold == 'SUPPORTED' and not contra and sim < 0.68:
        print(f'  MISSED: claim="{claim}"')
        print(f'  evidence="{ev}"')
        print(f'  sub_claims={sub_claims}')
