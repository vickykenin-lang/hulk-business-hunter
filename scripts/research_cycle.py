#!/usr/bin/env python3
"""HULK research-cycle bootstrap. Research only; never executes a business."""
import json, os
from datetime import datetime, timezone
from pathlib import Path
from soul_runtime import validate
ROOT=Path(__file__).resolve().parents[1]
MEM=ROOT/'data/memory.json'; CONTROL=ROOT/'data/control.json'; OUT=ROOT/'data/research_cycle_status.json'
def load(p,d):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except Exception:return d
def main():
    ok,soul=validate(); control=load(CONTROL,{}); mem=load(MEM,{})
    if control.get('kill_switch') or control.get('maintenance_pause') or not ok:
        state='BLOCKED'
    elif not control.get('research_execution_authorized',False): state='WAITING_AUTHORIZATION'
    else:
        # Lead-AI provider is credential-gated. No fabricated research is produced before a provider is configured.
        providers=[k for k in ('AWS_BEDROCK_API_KEY','DEEPSEEK_API_KEY','OPENAI_API_KEY') if os.getenv(k)]
        state='READY' if providers else 'WAITING_CREDENTIALS'
    result={'checked_at_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'state':state,'soul_valid':ok,'business_execution_authorized':False,'memory_status':mem.get('status'),'credential_values_stored':False}
    OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result));return 0
if __name__=='__main__':raise SystemExit(main())
