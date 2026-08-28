import io
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import research_cycle


class Response:
    def __init__(self,payload): self.payload=payload
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def read(self): return json.dumps(self.payload).encode()


class SearchApiHealthTests(unittest.TestCase):
    def test_missing_key(self):
        self.assertEqual(research_cycle.searchapi_health_check('')['health'],'CREDENTIAL_MISSING')

    def test_healthy_search(self):
        def opener(request,timeout):
            self.assertTrue(request.full_url.startswith(research_cycle.SEARCHAPI_ENDPOINT+'?'))
            self.assertEqual(timeout,20)
            self.assertEqual(request.headers['Authorization'],'Bearer test-secret')
            return Response({'organic_results':[{'title':'One'},{'title':'Two'}]})
        result=research_cycle.searchapi_health_check('test-secret',opener)
        self.assertEqual(result,{'health':'HEALTHY','result_count':2})

    def test_empty_results_are_not_healthy(self):
        result=research_cycle.searchapi_health_check('test-secret',lambda request,timeout:Response({}))
        self.assertEqual(result['health'],'EMPTY_RESULTS')


if __name__=='__main__': unittest.main()
