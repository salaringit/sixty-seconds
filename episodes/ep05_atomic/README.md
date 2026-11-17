# EP05 — Your view can corrupt data halfway through

**The problem**
Django autocommits every query, so if write #1 succeeds and write #2 raises, write #1 is already permanent.

**The fix**
`transaction.atomic()` — all of it, or none of it.

**The part tutorials skip**
Catch the exception OUTSIDE the block; queries issued in a broken transaction get refused. Never make network calls inside it, or you hold locks open. These tests use `TransactionTestCase`, because `TestCase` wraps each test in its own transaction and would hide the bug.

## Files

| File | What's in it |
|---|---|
| `demo.py` | the slow version and the fast version, side by side |
| `tests.py` | the proof — query counts asserted with `assertNumQueries` |

## Run it

```bash
python manage.py test episodes.ep05_atomic
```
