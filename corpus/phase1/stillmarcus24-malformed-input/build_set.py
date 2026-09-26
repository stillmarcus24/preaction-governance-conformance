import json, os, tanilo_receipt_verify as t
# Paths resolve from THIS FILE, not the cwd, so the script regenerates the same
# three files byte-identically from any working directory. (Reported by
# @TKCollective after an independent re-run: the previous version only resolved
# from corpus/phase1/ and gave a "file not found" anywhere else.)
HERE = os.path.dirname(os.path.abspath(__file__))
def out(name): return os.path.join(HERE, name)
VECTORS = {
 "env_not_object_string":      "not-an-envelope",
 "env_not_object_int":         12345,
 "env_null":                   None,
 "env_empty_object":           {},
 "signatures_string":          {"payload":"e30","signatures":"nope"},
 "signatures_int":             {"payload":"e30","signatures":7},
 "signatures_list_of_nondict": {"payload":"e30","signatures":["x",3]},
 "signatures_dict_not_list":   {"payload":"e30","signatures":{"a":1}},
 "payload_not_string_int":     {"payload":123,"signatures":[]},
 "payload_null":               {"payload":None,"signatures":[]},
 "payload_object":             {"payload":{"k":"v"},"signatures":[]},
 "missing_payload":            {"signatures":[]},
 "missing_signatures":         {"payload":"e30"},
 "signatures_empty_list":      {"payload":"e30","signatures":[]},
 "jws_not_object":             {"payload":"e30","jws":"str","signatures":[{"protected":"e30","signature":"x"}]},
}
# expected: the CONFORMANCE PROPERTY, in the draft vocabulary — a status, NEVER a raise.
# (draft-krausz-verification-state four-state vocab: valid|invalid|indeterminate|not_evaluated;
#  an exception is not one of the four, so a raise is a conformance FAILURE for any input.)
STATES = {"valid","invalid","indeterminate","not_evaluated"}
expected = {name: {"must_return_one_of": sorted(STATES), "must_not_raise": True,
                   "rationale": "malformed input is still input; a verifier that raises has opted out of the four-state vocabulary (draft §3.1)"}
            for name in VECTORS}
# RUN the reference implementation, record AS-RUN (never edited to match)
results = {}
for name, env in VECTORS.items():
    try:
        r = t.verify(env)
        # `errors` and `checks` are the verifier's own REASON — recorded as-run so the
        # file shows WHICH check each vector trips, not merely that it returned a status.
        # The conformance property is still status-only; a reason is diagnostic, never
        # normative, so a differing reason is not a conformance failure.
        results[name] = {"outcome":"returned","status":r.status,"indeterminate_reason":r.indeterminate_reason,
                         "reason":list(r.errors),"checks":dict(r.checks),"raised":False}
    except Exception as e:
        results[name] = {"outcome":"raised","exception":type(e).__name__+": "+str(e)[:80],"raised":True}
conforms = sum(1 for r in results.values() if not r["raised"])
json.dump(VECTORS, open(out("vectors.json"),"w"), indent=1)
json.dump(expected, open(out("expected.json"),"w"), indent=1)
json.dump({"implementation":"tanilo-receipt-verify==0.1.1","note":"as-run, not edited to match; failures would be reported",
           "reason_fields":"`reason` is the verifier's own errors list and `checks` its per-check map, both as-run. Diagnostic only: the conformance property in expected.json is status-only, so a different reason from another implementation is not a failure.",
           "conforming":conforms,"total":len(VECTORS),"results":results},
          open(out("results-tanilo-0.1.1.json"),"w"), indent=1)
print(f"packaged {len(VECTORS)} vectors | tanilo 0.1.1: {conforms}/{len(VECTORS)} return a status, {len(VECTORS)-conforms} raise")
