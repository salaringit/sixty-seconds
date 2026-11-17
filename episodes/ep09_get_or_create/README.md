# EP09 — get_or_create will create duplicates

**The problem**
It is a SELECT followed by an INSERT — two statements, with a race window between them.

**The fix**
A `UniqueConstraint` in `Meta.constraints`. The database refuses the second insert.

**The part tutorials skip**
`get_or_create` is only as safe as the constraint behind it. Prefer `UniqueConstraint` over `unique=True` — it supports multiple fields and conditional uniqueness. The INSERT is wrapped in a savepoint, so the real statement count is four, not two.

## Files

| File | What's in it |
|---|---|
| `demo.py` | the slow version and the fast version, side by side |
| `tests.py` | the proof — query counts asserted with `assertNumQueries` |

## Run it

```bash
python manage.py test episodes.ep09_get_or_create
```
