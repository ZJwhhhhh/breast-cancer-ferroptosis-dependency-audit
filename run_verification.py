#!/usr/bin/env python3
from pathlib import Path
import csv, json, math

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'data'/'audit'
summary=json.loads((AUDIT/'Final_Dependency_Audit_Summary.json').read_text(encoding='utf-8'))
with (AUDIT/'Final_Claim_Evidence_Table.csv').open(encoding='utf-8-sig',newline='') as f:
    claims=list(csv.DictReader(f))
checks={
 'candidate_reports': summary['candidate_reports']==63,
 'strict_reports': summary['strict_reports']==42,
 'claim_units': summary['claim_units']==20==len(claims),
 'independent_units_primary': summary['independent_units_primary']==sum(int(r['Independent_units_primary']) for r in claims)==37,
 'independent_units_sensitivity': summary['independent_units_sensitivity']==sum(int(r['Independent_units_sensitivity']) for r in claims)==39,
 'evidence_levels': summary['evidence_level_counts_primary']=={'E1':11,'E2':0,'E3':2,'E4':7},
 'raw_agreement': math.isclose(summary['raw_agreement'],45/62,rel_tol=0,abs_tol=1e-12),
}
for k,v in checks.items(): print(f"{k}: {'PASS' if v else 'FAIL'}")
if not all(checks.values()): raise SystemExit('Verification failed')
print('ALL LOCKED RESULTS VERIFIED')

