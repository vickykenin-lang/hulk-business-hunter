#!/usr/bin/env python3
"""HULK research-cycle bootstrap. Research only; never executes a business."""
import json, os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from soul_runtime import validate
ROOT=Path(__file__).resolve().parents[1]
MEM=ROOT/'data/memory.json'; CONTROL=ROOT/'data/control.json'; OUT=ROOT/'data/research_cycle_status.json'
SEARCHAPI_ENDPOINT='https://www.searchapi.io/api/v1/search'
SEARCH_PROBE_QUERY='India business opportunities market trends'
def load(p,d):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except Exception:return d

def searchapi_health_check(api_key, opener=urlopen):
    """Run a small authenticated search without returning or logging the key."""
    if not api_key:
        return {'health':'CREDENTIAL_MISSING','result_count':0}
    query=urlencode({'engine':'google','q':SEARCH_PROBE_QUERY})
    request=Request(f'{SEARCHAPI_ENDPOINT}?{query}',method='GET',headers={
        'Authorization':f'Bearer {api_key}',
        'Accept':'application/json',
    })
    try:
        with opener(request,timeout=20) as response:
            payload=json.loads(response.read().decode('utf-8'))
        organic=payload.get('organic_results') if isinstance(payload,dict) else None
        count=len(organic) if isinstance(organic,list) else 0
        return {'health':'HEALTHY' if count else 'EMPTY_RESULTS','result_count':count}
    except HTTPError as exc:
        return {'health':'FAILED','error_class':'HTTPError','http_status':exc.code,'result_count':0}
    except (URLError,TimeoutError) as exc:
        return {'health':'FAILED','error_class':type(exc).__name__,'result_count':0}
    except (ValueError,TypeError,UnicodeDecodeError) as exc:
        return {'health':'FAILED','error_class':type(exc).__name__,'result_count':0}

def main():
    ok,soul=validate(); control=load(CONTROL,{}); mem=load(MEM,{})
    search=searchapi_health_check(os.getenv('SERPER_API_KEY_HULK'))
    if control.get('kill_switch') or control.get('maintenance_pause') or not ok:
        state='BLOCKED'
    elif not control.get('research_execution_authorized',False): state='WAITING_AUTHORIZATION'
    else:
        # Lead-AI provider is credential-gated. No fabricated research is produced before a provider is configured.
        providers=[k for k in ('AWS_BEDROCK_API_KEY','DEEPSEEK_API_KEY','OPENAI_API_KEY') if os.getenv(k)]
        if not providers: state='WAITING_AI_CREDENTIAL'
        elif search['health']=='CREDENTIAL_MISSING': state='WAITING_SEARCH_CREDENTIAL'
        elif search['health']!='HEALTHY': state='SEARCH_DEGRADED'
        else: state='READY'
    result={'checked_at_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'state':state,'soul_valid':ok,'business_execution_authorized':False,'memory_status':mem.get('status'),'search_provider':'SEARCHAPI_IO','search_health':search,'credential_values_stored':False}
    OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result));return 0
if __name__=='__main__':raise SystemExit(main())
