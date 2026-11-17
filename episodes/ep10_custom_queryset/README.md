# EP10 — Delete your fat views with one class

**The problem**
The same filter chain copy-pasted into views, API, tasks and admin is four definitions of one business rule.

**The fix**
Subclass `models.QuerySet`, attach it with `PostQuerySet.as_manager()`.

**The part tutorials skip**
The methods chain because each returns a queryset — which is exactly what Manager methods cannot do.

## Files

| File | What's in it |
|---|---|
| `demo.py` | the slow version and the fast version, side by side |
| `tests.py` | the proof — query counts asserted with `assertNumQueries` |

## Run it

```bash
python manage.py test episodes.ep10_custom_queryset
```
