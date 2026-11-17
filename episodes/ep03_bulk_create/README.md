# EP03 — 1000 saves vs 1 query

**The problem**
A loop of `.create()` is one INSERT and one round trip each.

**The fix**
`bulk_create(..., batch_size=500)` — a single multi-row INSERT per batch.

**The part tutorials skip**
`save()` is not called and `pre_save`/`post_save` never fire. Primary keys are not populated on most backends (PostgreSQL is the exception).

## Files

| File | What's in it |
|---|---|
| `demo.py` | the slow version and the fast version, side by side |
| `tests.py` | the proof — query counts asserted with `assertNumQueries` |

## Run it

```bash
python manage.py test episodes.ep03_bulk_create
```
