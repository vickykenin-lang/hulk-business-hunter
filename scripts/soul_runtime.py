#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQ=[ROOT/'SOUL.md',ROOT/'OBJECTIVE.md',ROOT/'data/memory.json',ROOT/'data/control.json']
def load(p,d):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except Exception:return d
def validate():
    soul=(ROOT/'SOUL.md').read_text(encoding='utf-8') if (ROOT/'SOUL.md').exists() else ''
    obj=(ROOT/'OBJECTIVE.md').read_text(encoding='utf-8') if (ROOT/'OBJECTIVE.md').exists() else ''
    memory=load(ROOT/'data/memory.json',{})
    control=load(ROOT/'data/control.json',{})
    checks={
      'soul_present':bool(soul), 'objective_present':bool(obj),
      'memory_present':memory.get('engine')=='HULK', 'control_present':bool(control),
      'soul_contract':('fail closed' in soul.lower() and 'management' in soul.lower()),
      'objective_contract':('HULK OBJECTIVE' in obj and 'Evidence Discipline' in obj and 'Implementation Requirements & Credential Readiness' in obj),
      'execution_boundary':control.get('business_execution_authorized') is False,
      'hard_gate_declared':control.get('soul_gate_mode')=='hard_fail_closed'
    }
    valid=all(checks.values())
    out={'checked_at_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'valid':valid,'mode':'hard_fail_closed','checks':checks,'execution_effect':'RESEARCH_ALLOWED' if valid else 'AUTONOMOUS_RESEARCH_BLOCKED'}
    (ROOT/'data/soul_runtime_status.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    return valid,out
if __name__=='__main__':
    ok,out=validate();print(json.dumps(out));raise SystemExit(0 if ok else 2)
