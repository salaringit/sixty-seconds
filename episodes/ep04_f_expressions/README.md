# EP04 — This code silently loses data

**The problem**
`post.views = post.views + 1` reads in Python, so two concurrent requests both read the same value and one increment vanishes.

**The fix**
`F("views") + 1` — `SET views = views + 1`, done inside the database, atomically.

**The part tutorials skip**
After an `F()` update the in-memory instance is stale. Call `refresh_from_db()` if you need the new value. The test reproduces the lost update deterministically, no threads required.

## Files

| File | What's in it |
|---|---|
| `demo.py` | the slow version and the fast version, side by side |
| `tests.py` | the proof — query counts asserted with `assertNumQueries` |

## Run it

```bash
python manage.py test episodes.ep04_f_expressions
```
