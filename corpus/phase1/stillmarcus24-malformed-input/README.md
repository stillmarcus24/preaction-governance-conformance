# stillmarcus24 — malformed-input conformance set (Phase 1)

Tests the **instrument, not the receipt**: a conforming verifier must return one of the
four states (`valid` | `invalid` | `indeterminate` | `not_evaluated`) for *any* input,
including malformed input. An exception is not one of the four states — a verifier that
raises has silently opted out of the vocabulary it implements (draft-krausz-verification-state §3.1).

- `vectors.json` — 15 malformed envelopes (non-object envelope, `signatures` as string/int/
  dict/list-of-non-dict, non-string `payload`, missing members, non-object `jws`).
- `expected.json` — the conformance property per vector: must return one of the four states,
  must not raise.
- `results-tanilo-0.1.1.json` — reference results, **as-run, never edited to match**:
  `tanilo-receipt-verify==0.1.1` returns a status on **15/15**, raises on **0**
  (confirming the 0.1.0→0.1.1 fix). Any implementation that raises on these is reported as-run, failures included.
  Each result also carries the verifier's own `reason` (its `errors` list) and `checks` map, so the
  file shows *which* check a vector trips rather than only that it returned a status. Those two
  fields are **diagnostic, not normative** — the conformance property in `expected.json` is
  status-only, so another implementation reaching the same status by a different reason is
  conforming.
- `build_set.py` — regenerates all three files by running the reference verifier. Recompute it yourself.

## Reproducing

```sh
python3 -m venv .venv && .venv/bin/pip install 'tanilo-receipt-verify==0.1.1'
.venv/bin/python corpus/phase1/stillmarcus24-malformed-input/build_set.py
```

Output paths resolve from `build_set.py`'s own location, so it runs from **any** working
directory and rewrites the three files in place. (It previously resolved them from the cwd and
only worked when invoked from `corpus/phase1/` — reported by @TKCollective after an independent
re-run, fixed here.) `vectors.json` and `expected.json` regenerate byte-identically; only
`results-*.json` can change, and only if the verifier's behaviour changed.

CC0 1.0. Contributed to x402-foundation/tsc#4 Phase 1.
