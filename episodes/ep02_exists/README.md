# EP02 — `.count() > 0` is a bug

**The problem**
`.count()` makes the database count every matching row to answer a yes/no question.

**The fix**
`.exists()` — `SELECT 1 ... LIMIT 1`, stops at the first hit.

**The part tutorials skip**
The widely repeated claim that `.exists()` costs an extra query on an evaluated queryset is FALSE — Django reads `_result_cache` first, so both `.exists()` and `.count()` are free there. The real waste is checking with one queryset and then fetching the rows with a second one.

## Files

| File | What's in it |
|---|---|
| `demo.py` | the slow version and the fast version, side by side |
| `tests.py` | the proof — query counts asserted with `assertNumQueries` |

## Run it

```bash
python manage.py test episodes.ep02_exists
```
