# EP07 — You're loading 40 columns to show 2

**The problem**
`objects.all()` is `SELECT *` plus the cost of building a full model instance per row.

**The fix**
`only()`, `defer()`, or `values_list()` depending on what you actually need.

**The part tutorials skip**
`only()` keeps model instances — touch a deferred field and you get one extra query PER OBJECT. `values_list("x", flat=True)` skips model construction entirely.

## Files

| File | What's in it |
|---|---|
| `demo.py` | the slow version and the fast version, side by side |
| `tests.py` | the proof — query counts asserted with `assertNumQueries` |

## Run it

```bash
python manage.py test episodes.ep07_only_defer
```
